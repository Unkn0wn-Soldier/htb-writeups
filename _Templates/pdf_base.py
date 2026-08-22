#!/usr/bin/env python3
"""
pdf_base.py — Plantilla base para PDFs de teoría HTB · RedTeamLab César Contreras
──────────────────────────────────────────────────────────────────────────────────
REGLA DE ORO: código siempre en texto OSCURO sobre fondo CLARO.
Legible en pantalla, legible impreso en blanco/negro, sin pérdida de información.

Tamaño de página: 8.5" x 13" (Folio/Oficio) — fijado por acuerdo de trabajo.
Anti-overflow: las tablas SIEMPRE se arman con make_table() (celdas envueltas en
Paragraph, wrap real por palabra) y el código SIEMPRE se agrega con add_code_block()
(corta líneas largas antes de que se salgan del área imprimible). No pasar strings
crudos directo a Table() ni loops manuales de Preformatted() — así fue como Appointment
y Sequel v1 se desbordaron.

NO usar PageBreak() entre secciones. Dejar que el contenido fluya natural y que
reportlab corte página solo cuando el contenido no cabe — usar PageBreak() a mano
entre secciones cortas deja mitad de página en blanco (bug real en las primeras
versiones de Appointment/Sequel/Responder, corregido). Si una sección debe
empezar en página nueva por diseño (ej. portada sola), es la única excepción
razonable.

Uso:
    Copiar este archivo, cambiar OUTPUT y CONTENT, ejecutar con python3.
    Requiere: pip install reportlab --break-system-packages
"""

import textwrap

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Página ────────────────────────────────────────────────────────────────────
# 8.5 x 13 in (Folio/Oficio) — más alta que A4, aprovechar el espacio vertical extra
PAGE_SIZE   = (8.5 * inch, 13 * inch)
MARGIN_LR   = 2.0 * cm
MARGIN_TB   = 1.8 * cm
CONTENT_W   = PAGE_SIZE[0] - 2 * MARGIN_LR   # ancho útil real para tablas/código

# ── Paleta — SCREEN + PRINT SAFE ─────────────────────────────────────────────
RED     = colors.HexColor("#C62828")   # rojo oscuro (legible impreso)
DARK    = colors.HexColor("#1A1A1A")   # casi negro — texto principal
MID     = colors.HexColor("#37474F")   # gris azulado — cabeceras secundarias
ACCENT  = colors.HexColor("#BF360C")   # naranja oscuro — acentos
GREEN   = colors.HexColor("#1B5E20")   # verde oscuro — tips
ORANGE  = colors.HexColor("#E65100")   # naranja — advertencias

# Bloques de código: TEXTO OSCURO SOBRE FONDO GRIS CLARO — imprimible
CODE_FG = colors.HexColor("#1A1A1A")   # texto del código
CODE_BG = colors.HexColor("#F0F0F0")   # fondo gris claro

# Cajas especiales
WARN_FG = colors.HexColor("#7F0000")
WARN_BG = colors.HexColor("#FFEBEE")
TIP_FG  = GREEN
TIP_BG  = colors.HexColor("#E8F5E9")

# ── Estilos ───────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "title":  ParagraphStyle("TitleS", fontSize=26, fontName="Helvetica-Bold",
                                 textColor=RED, leading=31, spaceAfter=8, alignment=TA_CENTER),
        "sub":    ParagraphStyle("SubS",   fontSize=13, fontName="Helvetica",
                                 textColor=MID, leading=17, spaceBefore=4, spaceAfter=20,
                                 alignment=TA_CENTER),
        "h1":     ParagraphStyle("H1S",    fontSize=15, fontName="Helvetica-Bold",
                                 textColor=RED, leading=18, spaceBefore=18, spaceAfter=6,
                                 keepWithNext=True),
        "h2":     ParagraphStyle("H2S",    fontSize=12, fontName="Helvetica-Bold",
                                 textColor=DARK, leading=15, spaceBefore=12, spaceAfter=4,
                                 keepWithNext=True),
        "h3":     ParagraphStyle("H3S",    fontSize=10, fontName="Helvetica-Bold",
                                 textColor=MID, leading=13, spaceBefore=8, spaceAfter=3,
                                 keepWithNext=True),
        "body":   ParagraphStyle("BodyS",  fontSize=9.5, fontName="Helvetica",
                                 textColor=DARK, leading=15, spaceAfter=6,
                                 alignment=TA_JUSTIFY, wordWrap="CJK"),
        "bullet": ParagraphStyle("BulS",   fontSize=9.5, fontName="Helvetica",
                                 textColor=DARK, leading=15, spaceAfter=3,
                                 leftIndent=14, bulletIndent=0, wordWrap="CJK"),
        # CÓDIGO: Courier oscuro sobre fondo gris claro — legible en pantalla e impreso
        "code":   ParagraphStyle("CodeS",  fontSize=8.5, fontName="Courier",
                                 textColor=CODE_FG, backColor=CODE_BG,
                                 leading=13, spaceAfter=1,
                                 leftIndent=8, rightIndent=8),
        "warn":   ParagraphStyle("WarnS",  fontSize=9.5, fontName="Helvetica",
                                 textColor=WARN_FG, backColor=WARN_BG,
                                 leading=14, spaceAfter=4, leftIndent=8,
                                 wordWrap="CJK"),
        "tip":    ParagraphStyle("TipS",   fontSize=9.5, fontName="Helvetica",
                                 textColor=TIP_FG,  backColor=TIP_BG,
                                 leading=14, spaceAfter=4, leftIndent=8,
                                 wordWrap="CJK"),
        "footer": ParagraphStyle("FootS",  fontSize=8, fontName="Helvetica-Oblique",
                                 textColor=colors.grey, leading=10, alignment=TA_CENTER),
        "note":   ParagraphStyle("NoteS",  fontSize=9, fontName="Helvetica-Oblique",
                                 textColor=colors.grey, leading=11, alignment=TA_CENTER),
        # Celdas de tabla — SIEMPRE via make_table(), nunca strings crudos a Table()
        "cell_header": ParagraphStyle("CellHeadS", fontSize=8.5, fontName="Helvetica-Bold",
                                 textColor=colors.white, leading=10.5, wordWrap="CJK"),
        "cell":   ParagraphStyle("CellS",  fontSize=8.5, fontName="Helvetica",
                                 textColor=DARK, leading=11, wordWrap="CJK"),
        "cell_code": ParagraphStyle("CellCodeS", fontSize=7.5, fontName="Courier",
                                 textColor=DARK, leading=9.5, wordWrap="CJK"),
    }

def esc(text):
    """
    Escapa &, <, > en texto plano antes de pasarlo a Paragraph (que interpreta
    el string como XML). Usar siempre que el texto pueda contener '&' (ej.
    'ATT&CK', 'Tom & Jerry') o '<'/'>' fuera de un tag de formato intencional
    (<b>, <br/>). Si el texto ya trae tags de formato deliberados, NO usar esc()
    sobre el string completo — escapar solo la parte variable antes de insertarla.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#CCCCCC"), spaceAfter=6)

def table_style_base(header_color=MID):
    return TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), header_color),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0, 1), (-1,-1), [colors.white, colors.HexColor("#F5F5F5")]),
        ("GRID",          (0, 0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",    (0, 0), (-1,-1), 6),
        ("BOTTOMPADDING", (0, 0), (-1,-1), 6),
        ("LEFTPADDING",   (0, 0), (-1,-1), 7),
        ("RIGHTPADDING",  (0, 0), (-1,-1), 7),
        ("VALIGN",        (0, 0), (-1,-1), "TOP"),
    ])

def make_table(data, col_widths, styles, header=True, mono_cols=None, header_color=MID):
    """
    Construye una Table SIN riesgo de overflow: cada celda se envuelve en un
    Paragraph con wordWrap='CJK', que corta por palabra y, si una palabra/token
    es más ancha que la columna (rutas, URLs, comandos), corta por caracter en
    vez de desbordar fuera del borde de la celda.

    data:        lista de listas de strings — data[0] es encabezado si header=True
    col_widths:  lista de anchos (usar cm/inch). Debe sumar <= CONTENT_W.
    mono_cols:   set de índices de columna que deben renderizarse en Courier
                 (para celdas que contienen comandos/paths/código inline)
    """
    mono_cols = mono_cols or set()
    if sum(col_widths) - CONTENT_W > 0.2 * cm:
        raise ValueError(
            f"make_table: colWidths suman {sum(col_widths)/cm:.2f}cm, "
            f"excede el ancho útil de página ({CONTENT_W/cm:.2f}cm)."
        )

    wrapped = []
    for r, row in enumerate(data):
        wrapped_row = []
        for c, cell in enumerate(row):
            # esc() primero: si la celda trae '<IP>', '<tabla>', '&', etc. como
            # texto literal, sin esto Paragraph lo interpreta como tag XML y lo
            # descarta en silencio (bug real: '<IP>' desaparecía de celdas).
            text = esc(str(cell)).replace("\n", "<br/>")
            if header and r == 0:
                style = styles["cell_header"]
            elif c in mono_cols:
                style = styles["cell_code"]
            else:
                style = styles["cell"]
            wrapped_row.append(Paragraph(text, style))
        wrapped.append(wrapped_row)

    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(table_style_base(header_color))
    return t

def code_lines(text, max_chars=96):
    """
    Divide una línea de código larga en varias, respetando indentación,
    para que nunca se salga del área imprimible del bloque de código.
    Usado internamente por add_code_block() — no llamar Preformatted() a mano.
    """
    if len(text) <= max_chars:
        return [text]
    indent = len(text) - len(text.lstrip(" "))
    wrapped = textwrap.wrap(
        text, width=max_chars,
        subsequent_indent=" " * (indent + 4),
        break_long_words=True, break_on_hyphens=False,
        replace_whitespace=False, drop_whitespace=False,
    )
    return wrapped if wrapped else [text]

def add_code_block(story, styles, lines, max_chars=96):
    """
    Agrega un bloque de código a `story` línea por línea, envolviendo
    automáticamente cualquier línea que exceda max_chars (calculado para
    Courier 8.5pt dentro de CONTENT_W ≈ 96 caracteres). Reemplaza los loops
    manuales `for line in [...]: story.append(Preformatted(line, S["code"]))`.

    lines: lista de strings, o un solo string con '\n' como separador
    """
    if isinstance(lines, str):
        lines = lines.split("\n")
    for raw in lines:
        for sub in code_lines(raw, max_chars=max_chars):
            story.append(Preformatted(sub, styles["code"]))

def keep_section(*flowables):
    """Agrupa un heading con su primer contenido para evitar títulos huérfanos
    al final de página (viudas). Usar para h2/h3 + primer párrafo/tabla corta."""
    return KeepTogether(list(flowables))

def make_doc(output_path):
    return SimpleDocTemplate(
        output_path, pagesize=PAGE_SIZE,
        leftMargin=MARGIN_LR, rightMargin=MARGIN_LR,
        topMargin=MARGIN_TB, bottomMargin=MARGIN_TB
    )

def footer_line(styles, machine, date="2026"):
    return [
        HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=8),
        Paragraph(
            f"RedTeamLab · César Contreras · HTB {machine} · CPTS {date}",
            styles["footer"]
        )
    ]

# ── Ejemplo mínimo de uso ─────────────────────────────────────────────────────
if __name__ == "__main__":
    OUTPUT = "/tmp/test_base.pdf"
    S = make_styles()
    doc = make_doc(OUTPUT)
    story = []

    story.append(Paragraph("Máquina de Ejemplo", S["title"]))
    story.append(Paragraph("HTB Starting Point · Tier 0 · Página 8.5x13\"", S["sub"]))
    story.append(hr())

    story.append(Paragraph("1. Sección de ejemplo", S["h1"]))
    story.append(Paragraph("Texto de cuerpo legible en pantalla e impreso.", S["body"]))

    # Bloque de código — wrap automático de líneas largas, nunca se desborda
    add_code_block(story, S, [
        "nmap -sCV -p- --min-rate 5000 10.129.X.X -oN nmap.txt",
        "# Resultado:",
        "6379/tcp open  redis   Redis key-value store 5.0.7",
        "# Línea deliberadamente larga para probar el wrap automático de code_lines(): "
        "esto no debe salirse del área imprimible bajo ninguna circunstancia, ni con rutas largas como /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
    ])

    # Tabla — celdas con wrap real, ancho validado contra CONTENT_W
    story.append(Spacer(1, 0.3*cm))
    data = [
        ["Puerto", "Servicio", "Hallazgo clave"],
        ["6379/TCP", "Redis", "Sin autenticación — acceso directo con redis-cli sin credenciales, texto largo de prueba para forzar el wrap dentro de la celda"],
    ]
    story.append(make_table(data, [3*cm, 3.5*cm, CONTENT_W - 6.5*cm], S))

    story.append(Paragraph("⚠️  Advertencia importante aquí.", S["warn"]))
    story.append(Paragraph("💡  Tip o conexión con concepto mayor.", S["tip"]))

    story.extend(footer_line(S, "Ejemplo"))
    doc.build(story)
    print(f"Test PDF: {OUTPUT}")
