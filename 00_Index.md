# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026
> Certificación **CPTS (HTB)** antes de diciembre 2026 · OSCP+ en 2027 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso                                      |
| ------------------------------ | --------------------------------------------- |
| Máquinas HTB completadas      | 10 / 50                                       |
| Fase 0 — Starting Point       | 10 / 24 (Tier 0: 4/8 free completo · Tier 1: 5/9 · Tier 2: 1/7) |
| Writeups publicados en GitHub | 0                                              |
| Técnicas documentadas         | 11 — ver [[#Base de Técnicas]]                |
| Módulos CPTS completados      | En progreso                                   |
| Certificaciones obtenidas     | —                                              |

> [!danger] Alerta de ritmo
> Dancing se cerró el 2026-06-13. Appointment se retomó el 2026-08-10 — **48 días sin avance registrado** en medio. Desde la retomada (10-22 ago): 4 máquinas en 12 días, ritmo sostenido pero con una pausa notoria en Responder (iniciada 13-ago, cerrada 22-ago — 9 días, más lento que Appointment/Sequel/Crocodile por el atasco real con la IP de tun0 vs víctima). Sigue por detrás del roadmap (24 máquinas de Fase 0 pedidas para julio, van 8), la tendencia general es sana pero vigilar que Responder no marque un patrón de máquinas Windows/AD tomando más tiempo que las de Linux.

---

## Navegación Principal

- [[Roadmap_2026]] — Plan completo: Starting Point → Fases 1-3 → CPTS
- [[Metodologia_HTB]] — Protocolo de trabajo (45 min rule, flujo de ataque, writeups)
- [[Cheatsheet_Master]] — Comandos de referencia rápida por fase

### Directorios

- **HTB/** — Writeup de cada máquina (una carpeta por máquina, incluye PDF de teoría pre-máquina)
- **Técnicas/** — Base de conocimiento técnico por categoría, alimentada desde cada writeup
- **Certificaciones/** — Material de estudio CPTS / OSCP+ *(pendiente)*
- **Cheatsheets/** — Referencia rápida por herramienta *(pendiente)*
- **_Templates/** — Plantillas para máquinas, técnicas y generación de PDF

---

## Starting Point — Progreso

### Tier 0 (Free)

| #   | Máquina     | Estado      | Writeup                 | Técnica |
| --- | ----------- | ----------- | ------------------------ | ------- |
| 1   | Meow        | ✅ Terminada | [[HTB/Meow/Meow]]       | [[Técnicas/Default-Credentials]] |
| 2   | Fawn        | ✅ Terminada | [[HTB/Fawn/Fawn]]       | [[Técnicas/Default-Credentials]] |
| 3   | Dancing     | ✅ Terminada | [[HTB/Dancing/Dancing]] | [[Técnicas/SMB_Null_Session]] |
| 4   | Redeemer    | ✅ Terminada | [[HTB/Redeemer/Redeemer]] | [[Técnicas/Redis-Unauthenticated]] |
| 5   | Explosion   | 🔒 VIP+     | —                        | — |
| 6   | Preignition | 🔒 VIP+     | —                        | — |
| 7   | Mongod      | 🔒 VIP+     | —                        | — |
| 8   | Synced      | 🔒 VIP+     | —                        | — |

### Tier 1 (Free)

| #   | Máquina     | Estado       | Writeup                       | Técnica |
| --- | ----------- | ------------ | ------------------------------ | ------- |
| 9   | Appointment | ✅ Terminada | [[HTB/Appointment/Appointment]] | [[Técnicas/SQL-Injection]] |
| 10  | Sequel      | ✅ Terminada | [[HTB/Sequel/Sequel]]          | [[Técnicas/MySQL-Unauthenticated]] |
| 11  | Crocodile   | ✅ Terminada | [[HTB/Crocodile/Crocodile]]   | [[Técnicas/Credential-Reuse]] |
| 12  | Responder   | ✅ Terminada | [[HTB/Responder/Responder]]  | [[Técnicas/Forced-Authentication-SMB]] |
| 13  | Three       | ✅ Terminada | [[HTB/Three/Three]]           | [[Técnicas/AWS-S3-Misconfiguration]] |
| 14  | Ignition    | ⬜ Pendiente | —                               | — |
| 15  | Bike        | ⬜ Pendiente | —                               | — |
| 16  | Pennyworth  | ⬜ Pendiente | —                               | — |
| 17  | Tactics     | ⬜ Pendiente | —                               | — |

### Tier 2 (Free)

| #   | Máquina   | Estado       | Writeup |
| --- | --------- | ------------ | ------- |
| 18  | Archetype | ⬜ Pendiente | —       |
| 19  | Oopsie    | ⬜ Pendiente | —       |
| 20  | Vaccine   | ✅ Terminada | [[HTB/Vaccine/Vaccine]] |
| 21  | Unified   | ⬜ Pendiente | —       |
| 22  | Included  | ⬜ Pendiente | —       |
| 23  | Markup    | ⬜ Pendiente | —       |
| 24  | Base      | ⬜ Pendiente | —       |

---

## Base de Técnicas

Cada técnica documentada enlaza de vuelta a todas las máquinas donde se usó — el Graph View de Obsidian conecta automáticamente máquinas que comparten vector, sin mantenimiento manual adicional. Al cerrar una máquina nueva: si la técnica ya existe, solo agrega el wikilink en la sección "Conexiones" del writeup y una línea en "Dónde la usé" de la nota de técnica; si es nueva, créala con `[[_Templates/Technique_Template]]`.

| Técnica | Categoría MITRE | Máquinas que la usan |
| ------- | ---------------- | --------------------- |
| [[Técnicas/Default-Credentials]] | Initial Access (T1078.001) | Meow, Fawn |
| [[Técnicas/SMB_Null_Session]] | Lateral Movement (T1021.002) | Dancing |
| [[Técnicas/Redis-Unauthenticated]] | Initial Access (T1190) | Redeemer |
| [[Técnicas/SQL-Injection]] | Initial Access (T1190) | Appointment |
| [[Técnicas/MySQL-Unauthenticated]] | Initial Access (T1190) | Sequel |
| [[Técnicas/Credential-Reuse]] | Initial Access (T1078) | Crocodile |
| [[Técnicas/LLMNR-NBTNS-Poisoning]] | Credential Access (T1557.001) | (pendiente — teoría estudiada, sin máquina resuelta aún) |
| [[Técnicas/Forced-Authentication-SMB]] | Credential Access (T1187) | Responder |
| [[Técnicas/AWS-S3-Misconfiguration]] | Initial Access (T1190) | Three |
| [[Técnicas/SQLi-to-RCE-sqlmap]] | Initial Access / Execution (T1190) | Vaccine |
| [[Técnicas/GTFOBins-Sudo-Abuse]] | Privilege Escalation (T1548.003) | Vaccine |

---

## Últimas Máquinas Trabajadas

```dataview
TABLE ip, os, difficulty, status, tiempo
FROM "HTB"
SORT file.mtime DESC
LIMIT 10
```

---

## Técnicas Pendientes de Profundizar

```dataview
TASK
FROM "HTB"
WHERE !completed
LIMIT 20
```

---

## Registro Semanal

| Semana  | Máquinas         | Writeups | Técnica nueva aprendida |
| ------- | ----------------- | -------- | ------------------------- |
| Jun W1  | 1 (Meow)          | 1        | Telnet · default creds · MITRE T1078.001 |
| Jun W2  | 1 (Fawn)          | 1        | FTP anonymous login · CVE-1999-0497 · `get` vs shell |
| Jun W3  | 1 (Dancing)       | 1        | SMB null session · T1021.002 · smbclient shell escape (!cmd vs cmd) |
| Jun W4  | 1 (Redeemer)      | 1        | Redis sin auth · `INFO keyspace` antes de `KEYS *` |
| Jul     | 0                 | 0        | **Sin actividad registrada — 6 semanas** |
| Ago W2  | 3 (Appointment, Sequel, Crocodile) | 3 | SQLi login bypass · MySQL sin auth (`--skip-ssl`) · credential reuse cross-service (FTP → panel web) |
| Ago W3  | 1 (Responder) | 1 | LFI → Forced Authentication SMB (T1187, no T1557.001) · NetNTLMv2 + John · IP de payload = tun0 propia, no la víctima |
| Sep W1  | 1 (Three) | 1 | LocalStack expuesto sin auth (no S3/AWS real) · bucket = nombre del dominio · webshell PHP vía `aws s3 cp` · fingerprint por headers (`x-localstack-target`) antes de asumir el software |
| Sep W2  | 1 (Vaccine) | 1 | Primera cadena de 4 eslabones (no vector único) · `sqlmap --os-shell` depende de privilegios DB (superusuario Postgres) · orden estricto en estabilización TTY (`pty.spawn` ANTES de Ctrl+Z) · privesc vía GTFOBins (sudo sobre `vi`) |
