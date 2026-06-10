# 🧠 Perfil de Asesoría — César Contreras

> [!info] Documento interno de contexto
> Este archivo es para uso de la asesoría. Resume el perfil, objetivos, contexto y acuerdos de trabajo. Se actualiza cuando el contexto cambia significativamente.
> Última actualización: Junio 2026.

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

- **Formato por máquina:** teoría antes de la práctica (PDF o nota en vault), luego máquina, luego writeup mejorado con perspectiva defensiva + MITRE
- **Estándar de writeup:** el nivel del writeup de Meow es el mínimo aceptable
- **Ritmo de revisión:** cada 2 semanas revisar progreso contra el roadmap
- **Conexión Threat Hunting:** en cada máquina desde Tier 1 en adelante, añadir sección "¿Qué vería un Threat Hunter en este ataque?"
- **GitHub:** publicar writeups una vez la máquina sea retirada por HTB
- **Sin complacencia:** si el ritmo está por debajo del necesario, se dice directamente

---

## 10. Siguiente acción recomendada

1. **Hoy/mañana:** Hacer máquina Fawn con el PDF de teoría leído → writeup con template profesional
2. **Esta semana:** Completar Tier 0 (máquinas 2-8) — son rápidas, menos de 30 min cada una
3. **Antes del próximo viernes:** Primer commit en GitHub (aunque sea solo el writeup de Meow)
4. **Pendiente definir:** Qué es el Proyecto de Ingeniería universitario → evaluar si tiene sinergia con el vault
