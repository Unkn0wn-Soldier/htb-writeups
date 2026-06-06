---
tags:
  - htb
  - easy
  - en-progreso
  - windows
ip: 10.10.10.XXX
os: windows
difficulty: Easy
status: en-progreso
tiempo: 0h 0m
fecha_inicio: 2026-06-05
fecha_completada: —
puntos: 0
---
# 🖥️ [Lame] — [Windows] — [Easy]

> [!info] Resumen
> **IP:** `10.10.10.XXX`  |  **OS:** Linux/Windows  |  **Dificultad:** Easy/Medium/Hard
> **Estado:** En progreso  |  **Tiempo total:** Xh Xm

---

## 1. Reconocimiento

### Nmap — Puertos rápidos

```bash
nmap -sC -sV -oA nmap/inicial 10.10.10.XXX
nmap -p- --min-rate 5000 -oA nmap/full 10.10.10.XXX
```

**Puertos encontrados:**

| Puerto | Servicio | Versión | Notas |
| ------ | -------- | ------- | ----- |
| 22     | SSH      | OpenSSH X.X | — |
| 80     | HTTP     | Apache X.X | — |

### Reconocimiento Web

```bash
gobuster dir -u http://10.10.10.XXX -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
ffuf -u http://10.10.10.XXX/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
```

**Resultados relevantes:**

- `/admin` → Panel de administración (código 200)
- `/uploads` → Directorio de subida de archivos

### Otros servicios

> [!note] SMB / FTP / LDAP / Otros
> Anotar aquí lo relevante de servicios adicionales encontrados.

```bash
# SMB
smbclient -L //10.10.10.XXX -N
enum4linux -a 10.10.10.XXX

# FTP
ftp 10.10.10.XXX
```

---

## 2. Foothold

> [!warning] Punto de Entrada
> Describir aquí el vector de entrada principal. ¿Qué servicio? ¿Qué vulnerabilidad?

### Vulnerabilidad Identificada

**Nombre:** (ej. Shellshock, SQLi, File Upload bypass)  
**CVE:** CVE-XXXX-XXXXX (si aplica)  
**Por qué funciona:** Explicar el concepto con tus propias palabras.

### Exploit Utilizado

```bash
# Comando o script exacto que funcionó
# Agregar flags y parámetros usados
```

> [!tip] Lo que aprendí aquí
> Anotar aquí algo que no sabías antes de esta sección.

### Shell Obtenida

- **Usuario:** `www-data`
- **Tipo de shell:** bash / powershell / cmd
- **Estabilización de shell:**

```bash
# Estabilizar shell si es necesario
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z → stty raw -echo; fg
```

---

## 3. Escalación a Usuario (User Flag)

### Enumeración Post-Foothold

```bash
id; whoami; uname -a; hostname
cat /etc/passwd | grep -v nologin
cat /etc/cron* /etc/crontab /var/spool/cron/* 2>/dev/null
find / -perm -4000 2>/dev/null
sudo -l
env
```

**Hallazgos relevantes:**

- SUID encontrado: `...`
- Sudo permisos: `...`
- Archivos interesantes: `...`

### Método de Escalación a User

> [!success] Vector utilizado
> Describir el método con tus palabras. ¿Por qué fue posible? ¿Qué condición lo habilitó?

```bash
# Comandos exactos usados para escalar a user
```

### Flag de Usuario

```
user.txt → [CAPTURADA ✓]
```

---

## 4. Escalación a Root (Root Flag)

### Enumeración de Privesc

```bash
# Linux
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
# Windows
.\winPEAS.exe

# Manual rápido
find / -writable -type f 2>/dev/null | grep -v proc
ss -tulnp
cat /etc/sudoers 2>/dev/null
```

**Hallazgos relevantes:**

- `...`

### Método de Privesc a Root

> [!success] Vector utilizado
> Describir el método. ¿Por qué el sysadmin cometió ese error? ¿Cómo se hubiera prevenido?

```bash
# Comandos exactos para llegar a root
```

### Flag de Root

```
root.txt → [CAPTURADA ✓]
```

---

## 5. Lecciones Aprendidas

> [!danger] ¿Qué no sabía antes de esta máquina?
> - **Técnica X:** Explicar qué es y cómo funciona, en tus palabras.
> - **Tool Y:** Para qué sirve y cuándo usarla.

### ¿Dónde me bloqueé y por qué?

| Fase | Tiempo bloqueado | Causa real |
| ---- | ---------------- | ---------- |
| — | — | — |

### Técnicas a Profundizar

- [ ] Técnica X → Buscar en HackTricks
- [ ] Tool Y → Leer documentación oficial
- [ ] CVE Z → Entender el funcionamiento interno

### Herramientas Usadas

| Herramienta | Para qué la usé en esta máquina |
| ----------- | ------------------------------- |
| nmap | Reconocimiento de puertos |
| gobuster | Enumeración de directorios web |

### Conexión con Otras Máquinas / Técnicas

- Técnica similar a: `[[HTB/NombreMáquina/NombreMáquina]]`
- Ver también: `[[Técnicas/Nombre-Técnica]]`

---

## 6. Referencias

- [HackTricks - Nombre Técnica](https://book.hacktricks.xyz/)
- [CVE o Exploit utilizado](url)
- [Writeup oficial HTB](url)
- [IppSec video](https://ippsec.rocks/)
