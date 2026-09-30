# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026-2027
> Certificación **CPTS (HTB)** — ventana recalibrada abril-septiembre 2027 (ver [[Roadmap_2026]], recálculo 12-sep-2026) · OSCP+ movido a 2028 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso                                      |
| ------------------------------ | --------------------------------------------- |
| Máquinas HTB completadas      | 10 / 49 (Oopsie descartada el 12-sep-2026)    |
| Fase 0 — Starting Point       | 10 / 23 (Tier 0: 4/4 free alcanzable completo · Tier 1: 5/9 · Tier 2: 1/6) |
| HTB Academy — Penetration Tester Path | 0 / 28 módulos — inscrito 12-sep-2026, ~354h estimadas |
| Writeups publicados en GitHub | 0                                              |
| Técnicas documentadas         | 11 — ver [[#Base de Técnicas]]                |
| Certificaciones obtenidas     | —                                              |

> [!danger] Alerta de ritmo — recalibración 12-sep-2026
> Se descartó Oopsie (no se va a resolver) y se formalizó la inscripción al Academy Path CPTS (28 módulos, ~354h, gate obligatorio para rendir el examen). Con el ritmo real de 1-2h/día, la meta de "CPTS antes de diciembre 2026" quedó matemáticamente descartada — ni el path solo entra en los ~110 días que quedan del año. Nueva ventana objetivo: abril-septiembre 2027, detalle completo y fuentes en [[Roadmap_2026#Metodología de recálculo del ritmo (12-sep-2026)]]. Antes de este recálculo: Dancing se cerró 2026-06-13, hubo 48 días sin avance en julio, y desde la retomada (10-22 ago) el ritmo fue de 4 máquinas en 12 días — sano pero insuficiente para sostener la fecha original una vez se suma el peso real del Academy Path.

---

## Navegación Principal

- [[Roadmap_2026]] — Plan completo: Starting Point → Fases 1-3 → CPTS
- [[Metodologia_HTB]] — Protocolo de trabajo (45 min rule, flujo de ataque, writeups)
- [[Cheatsheet_Master]] — Comandos de referencia rápida por fase
- [[Recursos_GitHub_Baules]] — Repos y baúles de referencia para CPTS/OSCP

### Directorios

- **HTB/** — Writeup de cada máquina (una carpeta por máquina)
- **Técnicas/** — Base técnica **organizada por fase de ataque** (1_Reconocimiento → 7_Reporting)
- **Certificaciones/** — Checklists de estudio: [[Certificaciones/CPTS/README|CPTS]] · [[Certificaciones/OSCP/README|OSCP+]]
- **Cheatsheets/** — Referencia rápida por servicio/herramienta
- **_Templates/** — Plantillas para máquinas y técnicas

---

## Starting Point — Progreso

### Tier 0 (Free)

| #   | Máquina     | Estado      | Writeup                 | Técnica |
| --- | ----------- | ----------- | ------------------------ | ------- |
| 1   | Meow        | ✅ Terminada | [[HTB/Meow/Meow]]       | [[Técnicas/3_Explotación/Default-Credentials]] |
| 2   | Fawn        | ✅ Terminada | [[HTB/Fawn/Fawn]]       | [[Técnicas/3_Explotación/Default-Credentials]] |
| 3   | Dancing     | ✅ Terminada | [[HTB/Dancing/Dancing]] | [[Técnicas/2_Enumeración/SMB_Null_Session]] |
| 4   | Redeemer    | ✅ Terminada | [[HTB/Redeemer/Redeemer]] | [[Técnicas/3_Explotación/Redis-Unauthenticated]] |
| 5   | Explosion   | 🔒 VIP+     | —                        | — |
| 6   | Preignition | 🔒 VIP+     | —                        | — |
| 7   | Mongod      | 🔒 VIP+     | —                        | — |
| 8   | Synced      | 🔒 VIP+     | —                        | — |

### Tier 1 (Free)

| #   | Máquina     | Estado       | Writeup                       | Técnica |
| --- | ----------- | ------------ | ------------------------------ | ------- |
| 9   | Appointment | ✅ Terminada | [[HTB/Appointment/Appointment]] | [[Técnicas/3_Explotación/SQL-Injection]] |
| 10  | Sequel      | ✅ Terminada | [[HTB/Sequel/Sequel]]          | [[Técnicas/3_Explotación/MySQL-Unauthenticated]] |
| 11  | Crocodile   | ✅ Terminada | [[HTB/Crocodile/Crocodile]]   | [[Técnicas/3_Explotación/Credential-Reuse]] |
| 12  | Responder   | ✅ Terminada | [[HTB/Responder/Responder]]  | [[Técnicas/5_Active-Directory/Forced-Authentication-SMB]] |
| 13  | Three       | ✅ Terminada | [[HTB/Three/Three]]           | [[Técnicas/3_Explotación/AWS-S3-Misconfiguration]] |
| 14  | Ignition    | ⬜ Pendiente | —                               | — |
| 15  | Bike        | ⬜ Pendiente | —                               | — |
| 16  | Pennyworth  | ⬜ Pendiente | —                               | — |
| 17  | Tactics     | ⬜ Pendiente | —                               | — |

### Tier 2 (Free)

| #   | Máquina   | Estado       | Writeup |
| --- | --------- | ------------ | ------- |
| 18  | Archetype | ⬜ Pendiente | —       |
| 19  | ~~Oopsie~~ | ❌ Descartada (12-sep-2026) | — ver nota en [[Roadmap_2026#Fase 0 — Starting Point Free Tier (Junio 2026 – Noviembre 2026)]] |
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
| [[Técnicas/3_Explotación/Default-Credentials]] | Initial Access (T1078.001) | Meow, Fawn |
| [[Técnicas/2_Enumeración/SMB_Null_Session]] | Lateral Movement (T1021.002) | Dancing |
| [[Técnicas/3_Explotación/Redis-Unauthenticated]] | Initial Access (T1190) | Redeemer |
| [[Técnicas/3_Explotación/SQL-Injection]] | Initial Access (T1190) | Appointment |
| [[Técnicas/3_Explotación/MySQL-Unauthenticated]] | Initial Access (T1190) | Sequel |
| [[Técnicas/3_Explotación/Credential-Reuse]] | Initial Access (T1078) | Crocodile |
| [[Técnicas/5_Active-Directory/LLMNR-NBTNS-Poisoning]] | Credential Access (T1557.001) | (pendiente — teoría estudiada, sin máquina resuelta aún) |
| [[Técnicas/5_Active-Directory/Forced-Authentication-SMB]] | Credential Access (T1187) | Responder |
| [[Técnicas/3_Explotación/AWS-S3-Misconfiguration]] | Initial Access (T1190) | Three |
| [[Técnicas/3_Explotación/SQLi-to-RCE-sqlmap]] | Initial Access / Execution (T1190) | Vaccine |
| [[Técnicas/4_PrivEsc/GTFOBins-Sudo-Abuse]] | Privilege Escalation (T1548.003) | Vaccine |

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
| Sep W2  | 0 (recalibración) | 0 | Oopsie descartada · inscripción formal al Academy Path CPTS (28 módulos, ~354h) · roadmap y fecha objetivo recalculados de dic-2026 a abr-sep 2027 — ver [[Roadmap_2026]] |
