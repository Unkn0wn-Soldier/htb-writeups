# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026
> Certificación **CPTS (HTB)** antes de diciembre 2026 · OSCP+ en 2027 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso             |
| ----------------------------- | -------------------- |
| Máquinas HTB completadas      | 1 / 50               |
| Starting Point completadas    | 1 / 24 (Tier 0: 1/8) |
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
| 2   | Fawn        | ⬜ Pendiente | —                 |
| 3   | Dancing     | ⬜ Pendiente | —                 |
| 4   | Redeemer    | ⬜ Pendiente | —                 |
| 5   | Explosion   | ⬜ Pendiente | —                 |
| 6   | Preignition | ⬜ Pendiente | —                 |
| 7   | Mongod      | ⬜ Pendiente | —                 |
| 8   | Synced      | ⬜ Pendiente | —                 |

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
