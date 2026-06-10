# ⚙️ Metodología de Trabajo — HTB / Pentesting

> [!info] Propósito
> Este documento define cómo trabajar cada máquina para maximizar aprendizaje real, no solo capturar flags. La diferencia entre alguien que prepara CPTS y alguien que solo "completa máquinas" está en este protocolo.

---

## La Mentalidad Correcta

Antes de empezar cualquier máquina, interioriza esto:

- **El objetivo no es la flag.** Es entender por qué funcionó el ataque.
- **Atascarse es parte del proceso.** 45 minutos sin avance = revisa tu metodología, no busques writeups.
- **El writeup lo escribes TÚ primero.** Ver el oficial antes de intentarlo cancela el aprendizaje.
- **Un Red Teamer real no tiene hints.** Entrena como si no los hubiera.

---

## Flujo de Trabajo por Máquina

### Fase 1 — Setup (5 min)

```bash
# 1. Crear carpeta y archivo de notas
mkdir -p ~/HTB/<NombreMaquina>/nmap
cd ~/HTB/<NombreMaquina>

# 2. Añadir IP al /etc/hosts (si aplica)
echo "10.10.10.XXX <nombre>.htb" | sudo tee -a /etc/hosts

# 3. Conectar VPN HTB
sudo openvpn ~/htb.ovpn &
```

Crea el writeup en Obsidian **antes de empezar**. Escribe en tiempo real mientras hackeas — no al final.

---

### Fase 2 — Reconocimiento (no saltarse)

```bash
# Escaneo rápido de puertos (TCP)
nmap -p- --min-rate 5000 -oN nmap/ports_fast.txt <IP>

# Escaneo detallado solo en puertos encontrados
nmap -sC -sV -p <puertos> -oN nmap/detail.txt <IP>

# UDP (si nada funciona en TCP)
sudo nmap -sU --top-ports 20 <IP>
```

**Regla:** Documenta TODOS los puertos, aunque parezcan irrelevantes. El puerto que ignoraste es frecuentemente el vector.

#### Árbol de decisión post-nmap

```
Puerto 80/443 → Web recon (gobuster, whatweb, nikto)
Puerto 21     → FTP anónimo + credenciales por defecto
Puerto 22     → SSH (versión + user enum si es antigua)
Puerto 23     → Telnet + credenciales por defecto
Puerto 25/587 → SMTP (user enum, relay)
Puerto 139/445→ SMB (enum4linux, crackmapexec, smbclient)
Puerto 3306   → MySQL (login sin contraseña, credenciales por defecto)
Puerto 5985   → WinRM (evil-winrm si tienes credenciales)
Puerto 6379   → Redis (sin auth, info dump)
Puerto 27017  → MongoDB (sin auth, mongosh)
```

---

### Fase 3 — Enumeración Profunda

#### Web

```bash
# Directorios y archivos
gobuster dir -u http://<IP> -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -x php,html,txt,bak -o gobuster.txt

# Subdominios / vhosts
gobuster vhost -u http://<dominio>.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Tecnologías
whatweb http://<IP>
curl -I http://<IP>   # Headers

# Vulnerabilidades rápidas
nikto -h http://<IP> -o nikto.txt
```

#### SMB

```bash
smbclient -L //<IP> -N                         # Lista shares anónimo
smbmap -H <IP>                                 # Permisos por share
crackmapexec smb <IP>                          # Info del dominio
enum4linux -a <IP>                             # Enumeración completa
```

#### Servicios varios

```bash
# FTP anónimo
ftp <IP>   # usuario: anonymous, password: (enter vacío o email)

# Redis
redis-cli -h <IP> ping
redis-cli -h <IP> info

# MongoDB
mongosh <IP>:27017 --eval "show dbs"
```

---

### Fase 4 — Foothold

Una vez identificado el vector, documenta antes de explotar:

```
Vulnerabilidad: [nombre]
CVE (si aplica): CVE-XXXX-XXXXX
Por qué funciona: [en tus palabras, no copy-paste]
Herramienta/script: [nombre + flags exactos]
```

Si usas Metasploit, también documenta el módulo exacto y **entiende qué hace el exploit** antes de ejecutarlo.

#### Estabilización de shell (Linux)

```bash
# Si obtienes una shell no interactiva:
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z
stty raw -echo; fg
# Enter x2
```

---

### Fase 5 — Escalación de Privilegios

#### Linux — Checklist rápido

```bash
id; whoami; uname -a; hostname; cat /etc/os-release
sudo -l                          # Comandos sudo sin contraseña
find / -perm -4000 2>/dev/null   # Binarios SUID
cat /etc/crontab && ls /etc/cron.d/   # Cron jobs
ps aux                           # Procesos corriendo
ss -tulnp                        # Puertos internos
cat /etc/passwd | grep -v nologin
find / -writable -not -path "*/proc/*" 2>/dev/null
```

```bash
# LinPEAS (automatizado)
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh 2>/dev/null | tee linpeas.txt
```

#### Windows — Checklist rápido

```powershell
whoami /all
net localgroup administrators
systeminfo
tasklist /svc
netstat -ano
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue | Where-Object {$_.Name -like "*.txt" -or $_.Name -like "*.config"}
```

```powershell
# WinPEAS
.\winPEAS.exe > winpeas.txt
```

#### GTFOBins y recursos de referencia

- Linux privesc: [GTFOBins](https://gtfobins.github.io/)
- Windows privesc: [LOLBAS](https://lolbas-project.github.io/)
- Checklist completo: [HackTricks](https://book.hacktricks.xyz/)

---

## La Regla de los 45 Minutos

Cuando llevas 45 minutos sin avance en una fase específica:

1. **Para. Anota exactamente dónde estás atascado** y qué ya intentaste.
2. **Vuelve al reconocimiento.** La mayoría de los bloqueos son por información que faltó recopilar, no por falta de exploit.
3. **Lee HackTricks** para la tecnología/servicio específico que tienes — sin leer writeups aún.
4. **Usa el foro de HTB** (sin spoilers directos — busca hints conceptuales).
5. **Solo si pasas 90 minutos totales bloqueado:** mira el writeup oficial, pero *para en el paso que te trabó*, entiende el concepto, y continúa solo desde ahí.

> [!danger] Lo que NO debes hacer
> - Ver el writeup completo antes de intentar
> - Copiar comandos sin entender qué hacen
> - Saltar la enumeración porque "parece" que el vector es obvio

---

## Estructura del Writeup

Cada máquina debe tener su writeup en `HTB/<NombreMaquina>/<NombreMaquina>.md` usando el template en `_Templates/HTB_Template_Maquina.md`.

Un buen writeup incluye:
- **Contexto técnico:** por qué existe la vulnerabilidad
- **Comandos exactos usados** (con flags y parámetros)
- **Lo que NO funcionó** y por qué
- **Perspectiva defensiva:** cómo se detecta y remedia
- **MITRE ATT&CK mapping**
- **Conexión con otras técnicas/máquinas**

El writeup es para ti-del-futuro y para quien lea tu GitHub. Escríbelo como si el lector no hubiera visto la máquina.

---

## Publicación en GitHub

Cada writeup va al repositorio público después de que la máquina sea retirada (HTB la retira a la semana de expirar). Antes de publicar:

- [ ] Redacta o elimina flags reales (solo indica `[CAPTURADA ✓]`)
- [ ] Revisa que el writeup tenga sentido leído de corrido
- [ ] Añade capturas de pantalla de momentos clave si las tienes

---

## Métricas de Progreso

Actualiza `00_Index.md` al terminar cada máquina:
- Máquinas completadas / objetivo
- Tiempo promedio por máquina
- Técnicas nuevas aprendidas esa semana

Revisa el roadmap cada 2 semanas para ajustar el ritmo.
