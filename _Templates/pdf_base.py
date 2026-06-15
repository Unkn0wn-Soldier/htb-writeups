#!/usr/bin/env python3
"""
pdf_base.py — Plantilla base para PDFs de teoría HTB · RedTeamLab César Contreras
──────────────────────────────────────────────────────────────────────────────────
REGLA DE ORO: código siempre en texto OSCURO sobre fondo CLARO.
Legible en pantalla, legible impreso en blanco/negro, sin pérdida de información.

Uso:
    Copiar este archivo, cambiar OUTPUT y CONTENT, ejecutar con python3.
    Requiere: pip install reportlab --break-system-packages
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

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
                                 textColor=RED, spaceAfter=4, alignment=TA_CENTER),
        "sub":    ParagraphStyle("SubS",   fontSize=13, fontName="Helvetica",
                                 textColor=MID, spaceAfter=20, alignment=TA_CENTER),
        "h1":     ParagraphStyle("H1S",    fontSize=15, fontName="Helvetica-Bold",
                                 textColor=RED, spaceBefore=18, spaceAfter=6),
        "h2":     ParagraphStyle("H2S",    fontSize=12, fontName="Helvetica-Bold",
                                 textColor=DARK, spaceBefore=12, spaceAfter=4),
        "h3":     ParagraphStyle("H3S",    fontSize=10, fontName="Helvetica-Bold",
                                 textColor=MID, spaceBefore=8, spaceAfter=3),
        "body":   ParagraphStyle("BodyS",  fontSize=9.5, fontName="Helvetica",
                                 textColor=DARK, leading=15, spaceAfter=6,
                                 alignment=TA_JUSTIFY),
        "bullet": ParagraphStyle("BulS",   fontSize=9.5, fontName="Helvetica",
                                 textColor=DARK, leading=15, spaceAfter=3,
                                 leftIndent=14, bulletIndent=0),
        # CÓDIGO: Courier oscuro sobre fondo gris claro — legible en pantalla e impreso
        "code":   ParagraphStyle("CodeS",  fontSize=8.5, fontName="Courier",
                                 textColor=CODE_FG, backColor=CODE_BG,
                                 leading=13, spaceAfter=1,
                                 leftIndent=8, rightIndent=8),
        "warn":   ParagraphStyle("WarnS",  fontSize=9.5, fontName="Helvetica",
                                 textColor=WARN_FG, backColor=WARN_BG,
                                 leading=14, spaceAfter=4, leftIndent=8),
        "tip":    ParagraphStyle("TipS",   fontSize=9.5, fontName="Helvetica",
                                 textColor=TIP_FG,  backColor=TIP_BG,
                                 leading=14, spaceAfter=4, leftIndent=8),
        "footer": ParagraphStyle("FootS",  fontSize=8, fontName="Helvetica-Oblique",
                                 textColor=colors.grey, alignment=TA_CENTER),
        "note":   ParagraphStyle("NoteS",  fontSize=9, fontName="Helvetica-Oblique",
                                 textColor=colors.grey, alignment=TA_CENTER),
    }

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#CCCCCC"), spaceAfter=6)

def table_style_base(header_color=MID):
    return TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 8.5),
        ("FONTNAME",      (0, 1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1,-1), [colors.white, colors.HexColor("#F5F5F5")]),
        ("GRID",          (0, 0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",    (0, 0), (-1,-1), 5),
        ("BOTTOMPADDING", (0, 0), (-1,-1), 5),
        ("LEFTPADDING",   (0, 0), (-1,-1), 7),
        ("RIGHTPADDING",  (0, 0), (-1,-1), 7),
        ("VALIGN",        (0, 0), (-1,-1), "TOP"),
    ])

def make_doc(output_path):
    return SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm
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
    story.append(Paragraph("HTB Starting Point · Tier 0", S["sub"]))
    story.append(hr())

    story.append(Paragraph("1. Sección de ejemplo", S["h1"]))
    story.append(Paragraph("Texto de cuerpo legible en pantalla e impreso.", S["body"]))

    # Bloque de código — OSCURO SOBRE CLARO, siempre imprimible
    for line in [
        "nmap -sCV -p- --min-rate 5000 10.129.X.X -oN nmap.txt",
        "# Resultado:",
        "6379/tcp open  redis   Redis key-value store 5.0.7",
    ]:
        story.append(Preformatted(line, S["code"]))

    story.append(Paragraph("⚠️  Advertencia importante aquí.", S["warn"]))
    story.append(Paragraph("💡  Tip o conexión con concepto mayor.", S["tip"]))

    story.extend(footer_line(S, "Ejemplo"))
    doc.build(story)
    print(f"Test PDF: {OUTPUT}")
