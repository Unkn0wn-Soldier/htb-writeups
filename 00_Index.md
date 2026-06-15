# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026
> Certificación **CPTS (HTB)** antes de diciembre 2026 · OSCP+ en 2027 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso                                      |
| ----------------------------- | --------------------------------------------- |
| Máquinas HTB completadas      | 3 / 50                                        |
| Starting Point completadas    | 3 / 20 accesibles (Tier 0: 3/4 free · 4 VIP+) |
| Writeups publicados en GitHub | 0                    |
| Técnicas documentadas         | 0                    |
| Módulos CPTS completados      | En progreso          |
| Certificaciones obtenidas     | —                    |

---

## Navegación Principal

- [[Roadmap_2026]] — Plan completo: Starting Point → Fases 1-3 → CPTS
- [[Metodologia_HTB]] — Protocolo de trabajo (45 min rule, flujo de ataque, writeups)
- [[Cheatsheet_Master]] — Comandos de referencia rápida por fase

### Directorios

- **HTB/** — Writeup de cada máquina (una carpeta por máquina)
- **Técnicas/** — Base de conocimiento técnico por categoría *(pendiente de poblar)*
- **Certificaciones/** — Material de estudio CPTS / OSCP+ *(pendiente)*
- **Cheatsheets/** — Referencia rápida por herramienta *(pendiente)*
- **_Templates/** — Plantillas para máquinas y técnicas

---

## Starting Point — Progreso

### Tier 0 (Free)

| #   | Máquina     | Estado      | Writeup           |
| --- | ----------- | ----------- | ----------------- |
| 1   | Meow        | ✅ Terminada | [[HTB/Meow/Meow]] |
| 2   | Fawn        | ✅ Terminada | [[HTB/Fawn/Fawn]] |
| 3   | Dancing     | ✅ Terminada | [[HTB/Dancing/Dancing]] |
| 4   | Redeemer    | ⬜ Pendiente | —                 |
| 5   | Explosion   | 🔒 VIP+     | —                 |
| 6   | Preignition | 🔒 VIP+     | —                 |
| 7   | Mongod      | 🔒 VIP+     | —                 |
| 8   | Synced      | 🔒 VIP+     | —                 |

### Tier 1 (Free)

| # | Máquina | Estado | Writeup |
|---|---------|--------|---------|
| 9 | Appointment | ⬜ Pendiente | — |
| 10 | Sequel | ⬜ Pendiente | — |
| 11 | Crocodile | ⬜ Pendiente | — |
| 12 | Responder | ⬜ Pendiente | — |
| 13 | Three | ⬜ Pendiente | — |
| 14 | Ignition | ⬜ Pendiente | — |
| 15 | Bike | ⬜ Pendiente | — |
| 16 | Pennyworth | ⬜ Pendiente | — |
| 17 | Tactics | ⬜ Pendiente | — |

### Tier 2 (Free)

| # | Máquina | Estado | Writeup |
|---|---------|--------|---------|
| 18 | Archetype | ⬜ Pendiente | — |
| 19 | Oopsie | ⬜ Pendiente | — |
| 20 | Vaccine | ⬜ Pendiente | — |
| 21 | Unified | ⬜ Pendiente | — |
| 22 | Included | ⬜ Pendiente | — |
| 23 | Markup | ⬜ Pendiente | — |
| 24 | Base | ⬜ Pendiente | — |

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

| Semana | Máquinas | Writeups | Técnica nueva aprendida |
|--------|----------|----------|------------------------|
| Jun W1 | 1 (Meow) | 1 | Telnet · default creds · MITRE T1078.001 |
| Jun W2 | 1 (Fawn) | 1 | FTP anonymous login · CVE-1999-0497 · `get` vs shell |
| Jun W3 | 1 (Dancing) | 1 | SMB null session · T1021.002 · smbclient shell escape (!cmd vs cmd) |
