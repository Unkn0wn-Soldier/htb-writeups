# 📓 Guía Completa de Obsidian para Red Team

> [!info] Para quién es esta guía
> Red Teamer con tiempo limitado que necesita un sistema de notas que **funcione en el examen CPTS y OSCP+**, y que construya un portafolio técnico profesional en GitHub.

---

## Parte 1 — Estructura de la Bóveda

La bóveda es tu base de operaciones. Primero créala como una carpeta normal en tu sistema y luego ábrela desde Obsidian (File → Open Folder as Vault). Nombra la carpeta `RedTeam_Vault`.

La estructura que debes respetar:

```
RedTeam_Vault/
├── 00_Index.md                ← Dashboard principal (este archivo)
├── Roadmap_2026.md            ← Tu plan de certificaciones
├── Metodologia_HTB.md         ← Protocolo de trabajo
│
├── HTB/                       ← Una carpeta por máquina
│   ├── Lame/
│   │   ├── Lame.md            ← Writeup completo
│   │   └── img/               ← Screenshots de la máquina
│   ├── Blue/
│   │   ├── Blue.md
│   │   └── img/
│   └── ...
│
├── Técnicas/                  ← Base de conocimiento por categoría
│   ├── Reconocimiento/
│   │   ├── Nmap_avanzado.md
│   │   └── OSINT_pasivo.md
│   ├── Explotación/
│   │   ├── SQLi_manual.md
│   │   └── File_Upload_Bypass.md
│   ├── Privesc/
│   │   ├── Linux_SUID.md
│   │   └── Windows_Token_Impersonation.md
│   └── Active_Directory/
│       ├── Kerberoasting.md
│       ├── AS-REP_Roasting.md
│       └── Pass_the_Hash.md
│
├── Cheatsheets/               ← Referencia rápida (para el examen)
│   ├── Comandos_Linux.md
│   ├── Comandos_Windows.md
│   ├── Pivoting.md
│   └── AD_Attacks.md
│
└── Certificaciones/
    ├── CPTS/
    │   ├── Progreso_Modulos.md
    │   └── Notas_por_modulo/
    └── OSCP/
        └── (cuando llegue el momento)
```

---

## Parte 2 — Plugins Esenciales

Instálalos desde Settings → Community plugins → Browse.

### Plugins obligatorios

**Dataview** — Permite hacer consultas a tus notas como si fuera una base de datos. Es lo que hace funcionar las tablas automáticas del dashboard.

**Templater** — Reemplaza el sistema de plantillas básico de Obsidian. Permite insertar la fecha actual, el nombre del archivo y variables al crear una nota nueva desde una plantilla.

**Git** — Sincroniza tu bóveda con GitHub automáticamente. Configúralo para hacer commit cada vez que cierres Obsidian. Tus writeups quedan respaldados y públicos como portafolio.

**Calendar** — Agrega un pequeño calendario en el panel lateral. Útil para ver qué días trabajaste en HTB.

### Plugins recomendados

**Excalidraw** — Para dibujar diagramas de red dentro de Obsidian. Muy útil para mapear la topología de una red en el examen CPTS.

**Kanban** — Para trackear el estado de tus máquinas HTB visualmente (Por hacer / En progreso / Completada / Writeup publicado).

---

## Parte 3 — Configuración de Templater

### Paso 1 — Crear la carpeta de plantillas

Crea una carpeta llamada `_Templates/` en la raíz de tu bóveda y mueve ahí los archivos `HTB_Template_Maquina.md` y `Technique_Template.md`.

### Paso 2 — Configurar Templater

Ve a Settings → Templater:

- Template folder location: `_Templates`
- Trigger Templater on new file creation: **activado**
- Enable Folder Templates: **activado**
  - Asigna `HTB_Template_Maquina.md` a la carpeta `HTB/`
  - Asigna `Technique_Template.md` a la carpeta `Técnicas/`

Así, cada vez que crees una nota dentro de `HTB/`, la plantilla se aplicará automáticamente.

### Paso 3 — Variables útiles de Templater

Agrega estas variables en tus plantillas para que se rellenen solas:

```
Fecha actual:   <% tp.date.now("YYYY-MM-DD") %>
Nombre archivo: <% tp.file.title %>
```

---

## Parte 4 — Cómo Crear una Nota de Máquina (Flujo de trabajo)

Este es el flujo exacto que debes seguir cada vez que empieces una máquina HTB.

**Primero:** Crea la carpeta `HTB/NombreMaquina/` y dentro una subcarpeta `img/`.

**Segundo:** Crea el archivo `NombreMaquina.md` dentro de esa carpeta. Si tienes Templater configurado, la plantilla se aplica automáticamente.

**Tercero:** Rellena el frontmatter YAML con los datos de la máquina (IP, OS, dificultad). Esto es lo que Dataview usa para generar las tablas del dashboard.

**Cuarto:** Trabaja la máquina y documenta en tiempo real. No esperes terminar para tomar notas — escribe mientras hackeas.

**Quinto:** Después de rootear, escribe la sección de Lecciones Aprendidas. Este paso es el más importante y el que más gente omite.

**Sexto:** Crea notas individuales en `Técnicas/` para cada técnica nueva que hayas aprendido, y enlázala desde el writeup con `[[Técnicas/Nombre-Técnica]]`.

---

## Parte 5 — Sintaxis Obsidian que Necesitas Saber

### Callouts (cuadros de alerta)

```markdown
> [!info] Título opcional
> Contenido del cuadro.

> [!warning] Atención
> Algo importante o peligroso.

> [!success] Funcionó
> El exploit fue exitoso.

> [!danger] Error crítico
> Algo que no debes hacer.

> [!tip] Truco
> Consejo útil para recordar.
```

Tipos disponibles: `info`, `note`, `warning`, `danger`, `success`, `tip`, `abstract`, `bug`, `example`, `quote`.

### Links internos

```markdown
[[NombreNota]]                         ← Link a otra nota
[[NombreNota|Texto visible]]           ← Link con texto personalizado
![[NombreNota]]                        ← Embed (muestra el contenido)
![[img/screenshot.png]]                ← Embed de imagen
```

### Checkboxes de tareas

```markdown
- [ ] Tarea pendiente
- [x] Tarea completada
- [/] En progreso (plugin Tasks)
```

### Frontmatter YAML

```markdown
---
tags:
  - htb
  - linux
  - medium
ip: 10.10.10.XXX
status: rooteado
---
```

El frontmatter va siempre al inicio del archivo, entre los `---`. Dataview lo lee para generar consultas.

### Consulta Dataview básica


```dataview
TABLE ip, os, difficulty, status
FROM "HTB"
WHERE status = "rooteado"
SORT file.ctime DESC
```

---

## Parte 6 — Configurar Git para Publicar Writeups

### Prerequisito

Crea un repositorio en GitHub llamado `htb-writeups` (público). Los writeups públicos son tu portafolio técnico.

### Configuración en Obsidian

Settings → Git:

- Vault backup interval: `0` (manual o al cerrar)
- Auto pull interval: `0`
- Commit message: `writeup: {{date}} — {{hostname}}`

### En terminal, primera vez

```bash
cd ~/RedTeam_Vault
git init
git remote add origin https://github.com/tu-usuario/htb-writeups.git
git add .
git commit -m "init: vault structure"
git push -u origin main
```

Después, el plugin Git se encarga del resto.

---

## Parte 7 — Tips de Productividad

**Atajos de teclado que debes memorizar:**

| Atajo | Acción |
| ----- | ------ |
| `Ctrl + N` | Nueva nota |
| `Ctrl + O` | Abrir nota rápido |
| `Ctrl + P` | Paleta de comandos |
| `Ctrl + E` | Alternar edición / vista |
| `Ctrl + K` | Insertar link |
| `Alt + Enter` | Abrir link en panel dividido |

**Reglas de trabajo:**

Pon siempre `tags` en el frontmatter — es lo que permite filtrar con Dataview. Usa tags consistentes: `htb`, `linux`, `windows`, `easy`, `medium`, `hard`, `en-progreso`, `rooteado`, `writeup-publicado`.

Nunca dejes la sección "Lecciones Aprendidas" vacía. Si no tienes nada que escribir ahí, significa que no aprendiste nada nuevo — y eso es señal de que debes elegir máquinas más desafiantes.

Separa siempre el writeup de la máquina (en `HTB/`) de la nota de técnica (en `Técnicas/`). La nota de técnica debe poder entenderse independientemente de la máquina donde la aprendiste.
