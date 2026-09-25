# 🧠 Perfil de Asesoría — César Contreras

> [!info] Documento interno de contexto
> Este archivo es para uso de la asesoría. Resume el perfil, objetivos, contexto y acuerdos de trabajo. Se actualiza cuando el contexto cambia significativamente.
> Última actualización: 2026-09-17 — 10 máquinas terminadas. Oopsie descartada (12-sep-2026). Academy Path CPTS inscrito formalmente. Roadmap recalibrado: CPTS abril-septiembre 2027, OSCP+ 2028. Threat Hunting ya cursado y aprobado — ver nota en sección 3.

---

## 1. Objetivo del proceso

Formación técnica autodidacta en Red Team / Pentesting con doble propósito:
- **Corto plazo:** CPTS (HTB) — ventana recalibrada abril-septiembre 2027 (ver [[Roadmap_2026]])
- **Mediano plazo:** OSCP+ en 2028, primer empleo en pentesting/Red Team
- **Largo plazo:** Red Team Senior antes de los 30 + construcción de negocio propio de servicios ofensivos (Proyecto Cóndor)

---

## 2. Perfil del estudiante

| Campo | Detalle |
|-------|---------|
| **Nombre** | César Contreras |
| **Carrera** | Ingeniería en Ciberseguridad — CIISA |
| **Trimestre actual** | 8-9 (último tramo, titulación próxima ~2027) |
| **Situación** | Trabaja + estudia en paralelo |
| **Horas disponibles** | 6–10 horas semanales reales |
| **Nivel técnico** | Linux cómodo, nmap básico entendido, lógica de programación sí, scripting propio aún no |

---

## 3. Ramos universitarios actuales (relevantes)

| Ramo | Conexión con Red Team |
|------|-----------------------|
| **Taller de implementación de herramientas** | Media — depende del contenido específico del semestre |
| **Proyecto de Ingeniería** | Trabajo separado — carpeta distinta del vault |

> [!note] Threat Hunting — ya cursado y aprobado
> Ya no es ramo en curso. Es conocimiento adquirido. Decisión 25-sep-2026: **no se inyecta como sección "Threat Hunter" en los writeups** — el foco del vault es ofensivo (CPTS/OSCP). La detección/remediación mínima vive solo en la sección "Detección & Remediación".

> [!warning] Nota clave
> La enseñanza práctica en la universidad fue débil. César tiene vocabulario técnico de materias como Red Team ofensivo, Blue Team, Análisis de malware y Pentesting móvil/web — pero sin habilidad práctica real. **No asumir competencia técnica basada en los ramos cursados.**

---

## 4. Estilo de aprendizaje

- Necesita **concepto y lógica primero**, luego práctica
- Valora la **lectura de contexto** que profundiza el "por qué"
- No aprender bien solo con comandos sin entender qué hacen
- Ejemplo confirmado: pidió PDF teórico de FTP antes de hacer la máquina Fawn

---

## 5. Qué espera de la asesoría

- **Asesor metódico**, no solo fuente de información
- Que lo forme para **ser el mejor en su área**, no solo para pasar exámenes
- Que lo ayude a construir un **perfil diferenciado** en el mercado
- Que lo prepare para **entrevistas técnicas** y el entorno laboral real
- Que sus apuntes/writeups sean **utilizables en producción**, no solo académicos

---

## 6. Miedos reales (declarados)

1. Quedarse sin tiempo antes de estar listo
2. Llegar al examen CPTS sin conocimiento técnico suficiente
3. No encontrar trabajo al salir de la carrera
4. No llegar a Red Team Senior
5. Apuntes inútiles en entorno real
6. Mal rendimiento en entrevistas
7. Remuneraciones bajas

> [!danger] Riesgo principal identificado
> Todos estos miedos convergen en uno: **no construir habilidad real y demostrable a tiempo**. El antídoto es ritmo sostenido + documentación de calidad + visibilidad pública (GitHub, writeups).

---

## 7. Ambición de largo plazo

Crear un negocio propio de servicios de ciberseguridad ofensiva (**Proyecto Cóndor**). Diferenciación potencial para el mercado chileno/latinoamericano:
- Reporting en español con calidad internacional
- Conocimiento normativo local (NCG 461, ISO 27001, Ley Marco de Ciberseguridad Chile)
- Red Team as a Service con componente de automatización e IA
- Marca personal construida sobre writeups y certificaciones verificables

---

## 8. Riesgos y puntos ciegos identificados por el asesor

| Riesgo | Descripción | Mitigación |
|--------|-------------|------------|
| **Timeline recalibrado** | CPTS movido a abr-sep 2027 (matemáticamente imposible antes de dic-2026 con 1-2h/día). La meta es sostenible si se mantienen ~10h/semana. Ya hubo 48 días sin actividad en jul-2026 — riesgo real de repetición. | Revisión de ritmo cada 2 semanas contra Roadmap_2026.md. |
| **Visibilidad pública = 0** | 0 writeups en GitHub. Para el mercado laboral y para Cóndor, la marca personal es tan importante como la cert. | Empezar a publicar writeups de Starting Point cuando se retiren las máquinas |
| **Scripting gap** | Sin bash/python propio aún. No bloquea CPTS, pero sí limita capacidades avanzadas de Red Team (custom tooling, automatización) | Añadir ejercicios de scripting cortos ligados a máquinas que lo requieran |
| **Proyecto de titulación** | Carga adicional real que puede reducir las horas disponibles en trimestres clave | Monitorear carga universitaria — ajustar roadmap en octubre-noviembre si es necesario |

---

## 9. Acuerdos de trabajo

- **PDF antes de cada máquina:** detallado y explicativo — contexto, protocolo, herramientas, autoevaluación
- **Writeups:** concisos y precisos — solo lo necesario para resolver o revisar rápido en examen
  - Formato fijo: recon (tabla) → explotación (comandos) → MITRE (tabla) → detección/remediación (bullets) → lecciones (máx. 3)
  - Sin párrafos teóricos — eso va en el PDF
  - El asesor corrige errores técnicos del estudiante al pulir el writeup
- **Template activo:** `_Templates/HTB_Template_Maquina.md` (versión concisa, jun-2026)
- **Ritmo de revisión:** cada 2 semanas contra el roadmap
- **Sin complacencia:** si el ritmo cae, se dice directo
- **GitHub:** publicar writeups cuando la máquina sea retirada por HTB
- **Vault:** CLAUDE.md + Perfil + 00_Index se actualizan al cierre de cada sesión

---

## 10. Progreso y siguiente acción

**Completadas (10/49):** Meow ✅ · Fawn ✅ · Dancing ✅ · Redeemer ✅ (Tier 0: 4/4 free) · Appointment ✅ · Sequel ✅ · Crocodile ✅ · Responder ✅ · Three ✅ (Tier 1: 5/9) · Vaccine ✅ (Tier 2: 1/6).

**Descartada:** Oopsie ❌ (12-sep-2026) — se vio el writeup oficial antes de intentarla, cancela el aprendizaje.

**Estado Academy Path:** Inscrito 12-sep-2026 en Penetration Tester Job Role Path (28 módulos, ~354h). En curso: Penetration Testing Process (módulo 1, 46% completado al 17-sep-2026).

**Siguiente:**
1. Continuar Academy Path — Penetration Testing Process → módulos en secuencia
2. Próximas máquinas Fase 0: Ignition (Tier 1), luego Archetype (Tier 2)
3. GitHub: 10 writeups listos para publicar cuando HTB retire las máquinas
4. Threat Hunting ya cursado — NO se agrega sección Threat Hunter a los writeups (decisión 25-sep-2026); el foco es ofensivo
