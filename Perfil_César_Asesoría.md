# 🧠 Perfil de Asesoría — César Contreras

> [!info] Documento interno de contexto
> Este archivo es para uso de la asesoría. Resume el perfil, objetivos, contexto y acuerdos de trabajo. Se actualiza cuando el contexto cambia significativamente.
> Última actualización: 2026-06-11 — Sesión 1 completada. 2 máquinas SP Tier 0 terminadas.

---

## 1. Objetivo del proceso

Formación técnica autodidacta en Red Team / Pentesting con doble propósito:
- **Corto plazo:** CPTS (HTB) antes de diciembre 2026
- **Mediano plazo:** OSCP+ en 2027, primer empleo en pentesting/Red Team
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
| **Threat Hunting** | ⭐ Alta — entender qué detecta el Blue Team hace mejores atacantes. OPSEC y evasión se nutren de esto. |
| **Taller de implementación de herramientas** | Media — depende del contenido específico del semestre |
| **Proyecto de Ingeniería** | Trabajo separado — carpeta distinta del vault |

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
| **Timeline ajustado** | 6-10h/semana × 26 semanas = 156-260h totales. CPTS requiere 28 módulos + 40 máquinas. Es factible pero sin margen de error. | Revisión de ritmo cada 2 semanas. Ajustar roadmap si hay desvíos. |
| **Threat Hunting desaprovechado** | No conecta aún su ramo de Threat Hunting con OPSEC y evasión ofensiva | Integrar contenido del ramo en los writeups de HTB — qué detectaría un cazador en cada ataque |
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
- **Desde Tier 1:** añadir sección "¿Qué vería un Threat Hunter?" en cada writeup
- **Ritmo de revisión:** cada 2 semanas contra el roadmap
- **Sin complacencia:** si el ritmo cae, se dice directo
- **GitHub:** publicar writeups cuando la máquina sea retirada por HTB
- **Vault:** CLAUDE.md + Perfil + 00_Index se actualizan al cierre de cada sesión

---

## 10. Progreso y siguiente acción

**Completadas:** Meow ✅ · Fawn ✅ (2/24 SP Tier 0 · 2/50 total)

**Siguiente:**
1. Leer PDF teoría SMB (Dancing) → hacer Dancing → traer notas brutas
2. Completar Tier 0 antes de fin de junio (6 máquinas restantes)
3. Primer commit en GitHub pendiente — hacerlo al terminar Tier 0
4. Pendiente definir: sinergia Proyecto de Ingeniería con el vault
