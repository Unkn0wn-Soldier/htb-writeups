# Recursos GitHub — Baúles y Cheatsheets para CPTS / OSCP

> Repos y referencias para (a) copiar buenas estructuras de baúl y (b) estudiar para examen.
> **Verificar cada link antes de clonar** — los nombres de repo cambian. Buscar por el término si no resuelve.

## 1. Referencia técnica (los imprescindibles)

| Recurso | Qué es | Uso |
|---------|--------|-----|
| `swisskyrepo/PayloadsAllTheThings` | Payloads y one-liners por vulnerabilidad | Consulta rápida en explotación |
| `carlospolop/hacktricks` (book.hacktricks.xyz) | Enciclopedia de pentesting por servicio/fase | El mapa mental de todo el path |
| `GTFOBins/GTFOBins.github.io` | Abuso de binarios Unix para privesc | PrivEsc Linux |
| `LOLBAS-Project/LOLBAS` | Equivalente GTFOBins para Windows | PrivEsc Windows |
| `carlospolop/PEASS-ng` (linpeas/winpeas) | Enumeración automática de privesc | Post-explotación |

## 2. Cheatsheets / notas orientadas a CPTS

- Buscar en GitHub: `CPTS cheatsheet`, `HTB CPTS notes`, `Penetration Tester path notes`.
- Objetivo: ver cómo otros condensan cada módulo del Academy Path. **No copiar soluciones** — copiar la estructura de apuntes.

## 3. Notas / guías OSCP

- Buscar: `OSCP notes`, `OSCP cheatsheet`, `TJ Null OSCP list`.
- `0xsyr0/OSCP` y similares → cheat sheets extensos de comandos por fase.
- Lista de máquinas de TJ Null (HTB + Proving Grounds) → el estándar de práctica antes del examen.

## 4. Estructura de baúles Obsidian para pentest (para copiar el diseño)

- Buscar en GitHub: `pentest obsidian vault`, `obsidian pentest template`, `hacking notes obsidian`.
- Qué mirar al revisarlos:
  - Organización **por fase de ataque** (recon → enum → exploit → privesc → AD → reporting) ← ya lo aplicamos.
  - Uso de **templates** (Templater) y frontmatter YAML para metadatos de máquina.
  - **Graph view** para conectar máquinas por técnica compartida.
  - Dataview para dashboards de progreso.

## 5. Plantillas Notion (referencia de diseño, no para migrar)

- Buscar: `pentest notion template`, `OSCP notion tracker`.
- Útil solo para ideas de tablas de tracking (checklist de máquinas, estado, tiempo). El baúl vive en Obsidian.

---

## Siguiente acción concreta

1. Clonar/ojear `PayloadsAllTheThings` y `hacktricks` (los usarás en cada máquina).
2. Ver 1-2 baúles Obsidian de pentest y robar lo que te sirva de su estructura.
3. Instalar la skill `mattpocock/skills@obsidian-vault` para automatizar mantenimiento del baúl.
