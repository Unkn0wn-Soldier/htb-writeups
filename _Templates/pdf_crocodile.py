#!/usr/bin/env python3
"""
Guía BÁSICA — HTB Crocodile (Tier 1)
Técnica: FTP anónimo + reutilización de credenciales en panel web
RedTeamLab · César Contreras · CPTS 2026

Nota: a diferencia de los PDFs de Appointment/Sequel (detallados), este es
deliberadamente corto — solo lo esencial para encarar la máquina. Sin
PageBreak forzado: el contenido fluye natural, sin huecos en blanco.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_base import *

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "HTB", "Crocodile", "Guia_Basica_Crocodile.pdf"
)

S   = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1*cm))
story.append(Paragraph("HTB Crocodile — Tier 1", S["title"]))
story.append(Paragraph("Guía Básica · FTP Anónimo + Credential Reuse", S["sub"]))
story.append(hr())

# ── 1. Contexto ───────────────────────────────────────────────────────────────
story.append(Paragraph("1. Contexto de la Máquina", S["h1"]))
data = [
    ["Campo", "Detalle"],
    ["Tier / Fase",   "Tier 1 — Starting Point"],
    ["OS",            "Linux"],
    ["Dificultad",    "Easy"],
    ["Técnica clave", "FTP anónimo → credenciales encontradas → login en panel web"],
    ["Herramientas",  "nmap, ftp, gobuster/dirb, navegador o curl"],
]
story.append(make_table(data, [CONTENT_W*0.26, CONTENT_W*0.74], S))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "Crocodile combina dos servicios: FTP con login anónimo habilitado, y un "
    "panel web con formulario de login. El FTP no tiene la flag — tiene el "
    "material para entrar al panel. Es un ataque en dos pasos, no uno solo.",
    S["body"]
))

# ── 2. Idea central ───────────────────────────────────────────────────────────
story.append(Paragraph("2. Idea Central — Credential Reuse", S["h1"]))
story.append(Paragraph(
    "Un servicio sin autenticación (FTP anónimo) no siempre es el objetivo final: "
    "a veces es el punto de apoyo para comprometer OTRO servicio. Aquí el FTP "
    "expone archivos que contienen credenciales — la explotación real ocurre "
    "cuando esas credenciales se reutilizan en el panel web encontrado por "
    "enumeración de directorios.",
    S["body"]
))
story.append(Paragraph(
    "💡  Regla general: cuando un servicio sin auth entrega archivos de texto, "
    "revisar siempre su contenido antes de descartarlo — nombres de usuario, "
    "contraseñas, rutas internas o pistas del siguiente paso suelen estar ahí.",
    S["tip"]
))

# ── 3. Flujo de ataque ────────────────────────────────────────────────────────
story.append(Paragraph("3. Flujo de Ataque", S["h1"]))

story.append(Paragraph("3.1 Reconocimiento", S["h2"]))
add_code_block(story, S, [
    "nmap -sCV -p- --min-rate 5000 <IP> -oN nmap.txt",
    "# Esperado: 21/tcp (FTP) y 80/tcp (HTTP) abiertos",
])

story.append(Paragraph("3.2 FTP anónimo — obtener los archivos", S["h2"]))
add_code_block(story, S, [
    "ftp <IP>",
    "# Name: anonymous",
    "# Password: (Enter, vacío)",
    "",
    "ftp> ls -la",
    "ftp> get <archivo1>",
    "ftp> get <archivo2>",
    "",
    "# Revisar contenido en tu máquina:",
    "cat <archivo1>",
    "cat <archivo2>",
])
story.append(Paragraph(
    "Puede haber más de un archivo relevante — por ejemplo uno con nombres de "
    "usuario y otro con contraseñas. Revisar todo lo que el servidor entregue.",
    S["body"]
))

story.append(Paragraph("3.3 Enumerar el panel web", S["h2"]))
add_code_block(story, S, [
    "gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt -x php,html",
    "# Buscar en el output: una ruta de login/admin",
])

story.append(Paragraph("3.4 Probar las credenciales del FTP en el panel", S["h2"]))
add_code_block(story, S, [
    "# Ingresar al login encontrado con las credenciales extraídas del FTP",
    "# Si autentica → la flag suele estar directamente en el panel/dashboard",
])

# ── 4. MITRE ATT&CK ──────────────────────────────────────────────────────────
story.append(Paragraph("4. MITRE ATT&amp;CK", S["h1"]))
data2 = [
    ["Táctica", "Técnica", "ID"],
    ["Reconnaissance", "Active Scanning", "T1595"],
    ["Credential Access", "Unsecured Credentials", "T1552"],
    ["Initial Access", "Valid Accounts", "T1078"],
]
story.append(make_table(data2, [CONTENT_W*0.40, CONTENT_W*0.40, CONTENT_W*0.20], S))

# ── 5. Blue Team ──────────────────────────────────────────────────────────────
story.append(Paragraph("5. Blue Team — Lo Esencial", S["h1"]))
detect = [
    "Login `anonymous` en logs de FTP desde IP externa",
    "Login exitoso en el panel web justo después de la sesión FTP, misma IP — correlación temporal sospechosa",
    "Fix real: nunca credenciales en texto plano en un servicio sin auth, y nunca reutilizar contraseñas entre servicios",
]
for d in detect:
    story.append(Paragraph(f"• {d}", S["bullet"]))

# ── 6. Checklist ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("6. Checklist Rápida", S["h1"]))
data3 = [
    ["Paso", "Comando / Acción"],
    ["1. Recon",         "nmap -sCV -p- --min-rate 5000 <IP>"],
    ["2. FTP anónimo",   "ftp <IP> → anonymous / (vacío) → get de todo"],
    ["3. Revisar archivos", "cat de cada archivo descargado"],
    ["4. Enumerar web",  "gobuster dir -u http://<IP>/ -w common.txt"],
    ["5. Login",         "Probar credenciales del FTP en el panel encontrado"],
]
story.append(make_table(data3, [CONTENT_W*0.28, CONTENT_W*0.72], S, mono_cols={1}))

story.append(Spacer(1, 0.4*cm))
story.extend(footer_line(S, "Crocodile", "2026"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
