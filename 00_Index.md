# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026
> Certificación **CPTS (HTB)** antes de diciembre 2026 · OSCP+ en 2027 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso                                      |
| ------------------------------ | --------------------------------------------- |
| Máquinas HTB completadas      | 7 / 50                                        |
| Fase 0 — Starting Point       | 7 / 24 (Tier 0: 4/8 free completo · Tier 1: 3/9) |
| Writeups publicados en GitHub | 0                                              |
| Técnicas documentadas         | 7 — ver [[#Base de Técnicas]]                 |
| Módulos CPTS completados      | En progreso                                   |
| Certificaciones obtenidas     | —                                              |

> [!danger] Alerta de ritmo
> Dancing se cerró el 2026-06-13. Appointment se retomó el 2026-08-10 — **48 días sin avance registrado** en medio. Desde la retomada (10-13 ago): 3 máquinas en 4 días, ritmo sano. Sigue por detrás del roadmap (24 máquinas de Fase 0 pedidas para julio, van 7), pero la tendencia de esta semana es la que importa — sostenerla es lo que decide si Fase 0 se cierra a tiempo.

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
| 12  | Responder   | 🟡 En estudio | [[HTB/Responder/Responder]]  | LLMNR/NBT-NS poisoning · NTLMv2 |
| 13  | Three       | ⬜ Pendiente | —                               | — |
| 14  | Ignition    | ⬜ Pendiente | —                               | — |
| 15  | Bike        | ⬜ Pendiente | —                               | — |
| 16  | Pennyworth  | ⬜ Pendiente | —                               | — |
| 17  | Tactics     | ⬜ Pendiente | —                               | — |

### Tier 2 (Free)

| #   | Máquina   | Estado       | Writeup |
| --- | --------- | ------------ | ------- |
| 18  | Archetype | ⬜ Pendiente | —       |
| 19  | Oopsie    | ⬜ Pendiente | —       |
| 20  | Vaccine   | ⬜ Pendiente | —       |
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
| [[Técnicas/LLMNR-NBTNS-Poisoning]] | Credential Access (T1557.001) | Responder |

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
