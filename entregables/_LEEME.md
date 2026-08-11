# entregables/ — fuentes de este proyecto

Pon aquí tus documentos: **PDF, DOCX, XLSX, PPTX**.

Al abrir/retomar este proyecto en Claude Code, se genera automáticamente un espejo
`.md` en `../_md_export/` (Claude lee eso, no los PDF/Office crudos → ahorra tokens)
y graphify lo incorpora a su "cerebro" (`../graphify-out/`).

- Forzar conversión: `python C:\Users\hs\.claude\scripts\md_export.py "C:\RedTeamLab"`
- Reconstruir el cerebro: `/graphify` dentro del proyecto.
- Detalle de la convención: `~/.claude/PROJECT-BRAIN.md`.
