# 🔴 Red Team Vault — César Contreras

> [!info] Misión 2026
> Certificación **CPTS (HTB)** antes de diciembre 2026 · OSCP+ en 2027 · Red Team Senior a los 30.

---

## Estado Actual

| Métrica                       | Progreso    |
| ----------------------------- | ----------- |
| Máquinas HTB completadas      | 0 / 40      |
| Writeups publicados en GitHub | 0           |
| Técnicas documentadas         | 0           |
| Módulos CPTS completados      | En progreso |
| Certificaciones obtenidas     | —           |

---

## Navegación Principal

- [[Roadmap_2026]] — Plan de certificaciones y lista de máquinas específicas
- [[Metodologia_HTB]] — Protocolo de trabajo (45 min rule, hints, writeups)
- [[Cheatsheet_Master]] — Comandos de referencia rápida por categoría

### Directorios

- **HTB/** — Writeup de cada máquina (una carpeta por máquina)
- **Técnicas/** — Base de conocimiento técnico por categoría
- **Certificaciones/** — Material de estudio CPTS / OSCP+
- **Cheatsheets/** — Referencia rápida por herramienta o técnica

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

| Semana | Máquinas | Writeups | Notas clave |
| ------ | -------- | -------- | ----------- |
| —      | —        | —        | —           |
