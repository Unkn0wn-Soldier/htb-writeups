#!/usr/bin/env python3
"""
PDF de teoría — HTB Sequel (Tier 1)
Técnica principal: MySQL sin autenticación
RedTeamLab · César Contreras · CPTS 2026
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_base import *

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "HTB", "Sequel", "Teoria_MySQL_SinAuth.pdf"
)

S   = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph("HTB Sequel — Tier 1", S["title"]))
story.append(Paragraph("MySQL Sin Autenticación · Enumeración de Bases de Datos", S["sub"]))
story.append(hr())
story.append(Paragraph(
    "Este documento cubre la teoría necesaria para resolver Sequel: cómo funciona la "
    "autenticación en MySQL, qué pasa cuando falta, cómo enumerar bases de datos y tablas, "
    "qué detecta el Blue Team, y la conexión con Redeemer y con el CPTS.",
    S["body"]
))
story.append(Spacer(1, 0.5*cm))

# ── 1. Contexto de la Máquina ─────────────────────────────────────────────────
story.append(Paragraph("1. Contexto de la Máquina", S["h1"]))
story.append(hr())

data = [
    ["Campo", "Detalle"],
    ["Nombre",        "Sequel"],
    ["Tier / Fase",   "Tier 1 — Starting Point"],
    ["OS",            "Linux"],
    ["Dificultad",    "Easy"],
    ["Técnica clave", "MySQL sin autenticación — acceso root sin contraseña"],
    ["Herramientas",  "nmap, mysql client"],
    ["Vector",        "Servicio MySQL expuesto en 3306 con root sin password"],
]
story.append(make_table(data, [CONTENT_W*0.28, CONTENT_W*0.72], S))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph(
    "Sequel expone un servidor MySQL en el puerto 3306 donde la cuenta root no tiene "
    "contraseña asignada. No hay exploit ni bypass — es autenticación legítima con campo "
    "vacío. El objetivo: conectar, enumerar bases de datos y extraer la flag.",
    S["body"]
))
story.append(Paragraph(
    "💡  Conexión directa con Redeemer: mismo patrón — servicio de almacenamiento de datos "
    "(Redis allá, MySQL acá) expuesto sin autenticación. El flujo mental es idéntico: "
    "conectar, enumerar estructura, extraer datos. Solo cambia la sintaxis del cliente.",
    S["tip"]
))

# ── 2. MySQL — Fundamentos de Autenticación ──────────────────────────────────
story.append(Paragraph("2. MySQL — Fundamentos de Autenticación", S["h1"]))
story.append(hr())

story.append(Paragraph("2.1 ¿Cómo autentica MySQL normalmente?", S["h2"]))
story.append(Paragraph(
    "MySQL valida cada conexión contra la tabla interna <b>mysql.user</b>, que almacena "
    "usuario, host permitido, y hash de contraseña. Si el campo de contraseña está vacío "
    "para una cuenta, el servidor acepta la conexión sin exigir credencial — no es un bug, "
    "es el comportamiento documentado cuando no se configura contraseña.",
    S["body"]
))

story.append(Paragraph("2.2 ¿Por qué ocurre en la práctica?", S["h2"]))
causes = [
    "Instalación rápida en entorno de desarrollo/testing que se despliega a producción sin hardening",
    "Contenedor Docker con imagen MySQL sin variable MYSQL_ROOT_PASSWORD definida",
    "Migración de datos donde se resetea la contraseña y se olvida reconfigurarla",
    "Configuración de <b>bind-address</b> apuntando a 0.0.0.0 en vez de 127.0.0.1 — expone el servicio más allá de localhost",
]
for c in causes:
    story.append(Paragraph(f"• {c}", S["bullet"]))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph(
    "⚠️  Este es uno de los hallazgos más comunes en pentests reales de infraestructura — "
    "bases de datos de desarrollo que terminan expuestas en producción sin que nadie revise "
    "la configuración de autenticación antes del despliegue.",
    S["warn"]
))

story.append(Paragraph("2.3 Estructura de MySQL — Jerarquía de Datos", S["h2"]))
add_code_block(story, S, [
    "MySQL Server",
    "  └── Database (schema)      -- ej: 'htb', 'information_schema', 'mysql'",
    "        └── Table              -- ej: 'users', 'flags'",
    "              └── Row / Record  -- cada fila de datos",
    "                    └── Column   -- cada campo dentro de una fila",
])

story.append(Paragraph(
    "A diferencia de Redis (clave-valor plano), MySQL es relacional: hay que navegar "
    "database → table → rows antes de llegar al dato. Es un nivel más de estructura, "
    "pero el flujo de enumeración es igual de directo sin autenticación de por medio.",
    S["body"]
))

# ── 3. Reconocimiento Pre-Explotación ────────────────────────────────────────
story.append(Paragraph("3. Reconocimiento Pre-Explotación", S["h1"]))
story.append(hr())

story.append(Paragraph("3.1 Nmap — Identificar y Fingerprint MySQL", S["h2"]))
add_code_block(story, S, [
    "nmap -sCV -p- --min-rate 5000 <IP> -oN nmap_sequel.txt",
    "",
    "# Qué buscar en output:",
    "# 3306/tcp open  mysql   MySQL 5.5.5-10.3.X-MariaDB-...",
    "",
    "# Scripts NSE específicos para MySQL:",
    "nmap -p 3306 --script mysql-info,mysql-empty-password <IP>",
    "",
    "# mysql-empty-password confirma directamente si root acepta conexión sin clave",
])

story.append(Paragraph("3.2 Instalar Cliente MySQL (si falta)", S["h2"]))
add_code_block(story, S, [
    "# Debian/Ubuntu/Kali:",
    "sudo apt install mysql-client -y",
    "",
    "# Verificar instalación:",
    "mysql --version",
])

# ── 4. Explotación — Enumeración MySQL ───────────────────────────────────────
story.append(Paragraph("4. Explotación — Enumeración MySQL", S["h1"]))
story.append(hr())

story.append(Paragraph("4.1 Conexión Inicial", S["h2"]))
add_code_block(story, S, [
    "mysql -h <IP> -u root",
    "",
    "# Si conecta sin pedir password → confirmado vulnerable",
    "# Prompt resultante:",
    "# mysql>",
])

story.append(Paragraph("4.2 Enumeración Sistemática", S["h2"]))
add_code_block(story, S, [
    "-- Paso 1: listar todas las bases de datos disponibles",
    "SHOW DATABASES;",
    "",
    "-- Output típico:",
    "-- +--------------------+",
    "-- | Database           |",
    "-- +--------------------+",
    "-- | information_schema |",
    "-- | htb                |   <- BD de interés, no es de sistema",
    "-- | mysql              |",
    "-- | performance_schema |",
    "-- +--------------------+",
    "",
    "-- Paso 2: seleccionar la BD relevante (ignorar las de sistema)",
    "USE htb;",
    "",
    "-- Paso 3: listar tablas dentro de esa BD",
    "SHOW TABLES;",
    "",
    "-- Paso 4: inspeccionar estructura de una tabla antes de leerla",
    "DESCRIBE <nombre_tabla>;",
    "",
    "-- Paso 5: extraer todos los datos",
    "SELECT * FROM <nombre_tabla>;",
])

story.append(Paragraph(
    "💡  Ignorar siempre <b>information_schema</b>, <b>mysql</b>, y <b>performance_schema</b> "
    "en la primera pasada — son bases de datos internas del motor, no contienen datos de la "
    "aplicación objetivo. La BD relevante suele tener un nombre descriptivo del contexto de la máquina.",
    S["tip"]
))

story.append(Paragraph("4.3 Alternativa: Enumeración en Un Solo Comando", S["h2"]))
add_code_block(story, S, [
    "# Ejecutar query sin entrar al prompt interactivo (-e = execute)",
    "mysql -h <IP> -u root -e \"SHOW DATABASES;\"",
    "",
    "mysql -h <IP> -u root -e \"USE htb; SHOW TABLES;\"",
    "",
    "mysql -h <IP> -u root -e \"USE htb; SELECT * FROM users;\"",
])

# ── 5. MITRE ATT&CK ──────────────────────────────────────────────────────────
story.append(Paragraph("5. MITRE ATT&amp;CK — Mapeo de la Técnica", S["h1"]))
story.append(hr())

data3 = [
    ["Táctica", "Técnica", "ID", "Descripción"],
    ["Reconnaissance", "Active Scanning", "T1595",
     "nmap identifica MySQL en 3306 y confirma ausencia de password"],
    ["Initial Access", "Exploit Public-Facing Application", "T1190",
     "Conexión root sin credenciales a servicio expuesto públicamente"],
    ["Credential Access", "Unsecured Credentials", "T1552",
     "Si las tablas contienen credenciales de aplicación en texto plano"],
]
story.append(make_table(
    data3,
    [CONTENT_W*0.20, CONTENT_W*0.28, CONTENT_W*0.12, CONTENT_W*0.40],
    S
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "T1552 aplica solo si las tablas enumeradas contienen credenciales reutilizables — "
    "por ejemplo, contraseñas de usuarios de un panel web asociado. Verificar siempre "
    "el contenido de tablas tipo 'users' o 'accounts' con esa hipótesis en mente.",
    S["body"]
))

# ── 6. Blue Team — Detección ─────────────────────────────────────────────────
story.append(Paragraph("6. Blue Team — ¿Qué se Detecta?", S["h1"]))
story.append(hr())

story.append(Paragraph("6.1 Logs de MySQL", S["h2"]))
add_code_block(story, S, [
    "-- Habilitar general query log (si no está activo, esto es post-incidente):",
    "SET GLOBAL general_log = 'ON';",
    "SET GLOBAL general_log_file = '/var/log/mysql/query.log';",
    "",
    "-- Buscar conexiones root sin autenticación previa exitosa fallida:",
    "grep 'Connect.*root@' /var/log/mysql/query.log",
    "",
    "-- Señal clave: Connect exitoso inmediato sin intentos fallidos previos",
    "-- = credencial vacía, no fuerza bruta",
])

story.append(Paragraph("6.2 Indicadores de Red", S["h2"]))
detection_items = [
    "<b>Firewall/IDS:</b> conexiones entrantes al puerto 3306 desde IPs fuera del rango de aplicaciones autorizadas",
    "<b>NetFlow/Zeek:</b> tráfico MySQL (protocolo binario propio) sin TLS — datos en texto plano visibles en captura",
    "<b>SIEM:</b> correlacionar IP origen de conexión MySQL con lista de hosts de aplicación esperados — cualquier IP fuera de esa lista es anómala",
]
for item in detection_items:
    story.append(Paragraph(f"• {item}", S["bullet"]))

story.append(Paragraph("6.3 Perspectiva Threat Hunter", S["h2"]))
story.append(Paragraph(
    "A diferencia de SQLi (que deja huella en logs de aplicación web con payloads "
    "sospechosos), el acceso a MySQL sin contraseña es indistinguible de una conexión "
    "administrativa legítima a nivel de protocolo. La única señal es <b>origen de red</b>: "
    "si la conexión viene de una IP que no es el servidor de aplicación esperado, es anómala. "
    "Sin logging de origen o segmentación de red, este vector es completamente silencioso.",
    S["body"]
))
story.append(Paragraph(
    "⚠️  Esto refuerza un punto de OPSEC ofensivo: servicios de datos sin auth expuesta "
    "son de los vectores más limpios — no generan errores, no disparan WAFs, no dejan "
    "payloads sospechosos. El único rastro es la conexión de red en sí.",
    S["warn"]
))

# ── 7. Remediación ───────────────────────────────────────────────────────────
story.append(Paragraph("7. Remediación — Cómo se Parchea", S["h1"]))
story.append(hr())

story.append(Paragraph("7.1 Asignar Contraseña (fix principal)", S["h2"]))
add_code_block(story, S, [
    "-- MySQL 5.7+ / MariaDB:",
    "ALTER USER 'root'@'localhost' IDENTIFIED BY 'ContraseñaFuerte123!';",
    "",
    "-- Si root acepta conexiones remotas (host = '%'), también:",
    "ALTER USER 'root'@'%' IDENTIFIED BY 'ContraseñaFuerte123!';",
    "",
    "-- Aplicar cambios:",
    "FLUSH PRIVILEGES;",
])

story.append(Paragraph("7.2 Restringir Exposición de Red", S["h2"]))
add_code_block(story, S, [
    "# En my.cnf / mysqld.cnf:",
    "[mysqld]",
    "bind-address = 127.0.0.1",
    "",
    "# Si se requiere acceso remoto legítimo (ej. app en otro host):",
    "# usar un usuario dedicado con privilegios mínimos, NUNCA root remoto",
    "# y restringir el host de origen explícitamente:",
    "CREATE USER 'app_user'@'10.0.0.5' IDENTIFIED BY 'clave_fuerte';",
    "GRANT SELECT, INSERT ON app_db.* TO 'app_user'@'10.0.0.5';",
])

story.append(Paragraph("7.3 Otras mitigaciones complementarias", S["h2"]))
mitigations = [
    "<b>Least privilege:</b> cuentas de aplicación nunca deben usar root — privilegios mínimos por tabla/operación",
    "<b>Firewall:</b> bloquear 3306 desde Internet; permitir solo desde IPs de aplicación conocidas",
    "<b>Auditoría:</b> habilitar MySQL Enterprise Audit o general_log en entornos críticos",
    "<b>Rotación:</b> política de rotación periódica de contraseñas de servicio",
    "<b>Deshabilitar FILE privilege:</b> salvo necesidad explícita, previene lectura/escritura de archivos vía SQL",
]
for m in mitigations:
    story.append(Paragraph(f"• {m}", S["bullet"]))

# ── 8. Cheatsheet Rápida ─────────────────────────────────────────────────────
story.append(Paragraph("8. Cheatsheet — Sequel", S["h1"]))
story.append(hr())

story.append(Paragraph("Flujo de ataque completo:", S["h2"]))
add_code_block(story, S, [
    "# 1. Reconocimiento",
    "nmap -sCV -p- --min-rate 5000 <IP> -oN nmap.txt",
    "nmap -p 3306 --script mysql-info,mysql-empty-password <IP>",
    "",
    "# 2. Conectar",
    "mysql -h <IP> -u root",
    "",
    "# 3. Enumerar (dentro del prompt mysql>)",
    "SHOW DATABASES;",
    "USE <db_relevante>;",
    "SHOW TABLES;",
    "SELECT * FROM <tabla>;",
    "",
    "# 4. Alternativa en una línea (sin prompt interactivo)",
    "mysql -h <IP> -u root -e \"SHOW DATABASES;\"",
    "",
    "# 5. Buscar flag directamente si se sospecha el nombre de tabla/columna",
    "mysql -h <IP> -u root -e \"USE htb; SELECT * FROM flag;\"",
])

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Comandos MySQL de referencia rápida:", S["h2"]))
data4 = [
    ["Comando", "Función"],
    ["SHOW DATABASES;",        "Listar todas las bases de datos"],
    ["USE <db>;",              "Seleccionar una base de datos"],
    ["SHOW TABLES;",           "Listar tablas de la BD seleccionada"],
    ["DESCRIBE <tabla>;",      "Ver estructura/columnas de una tabla"],
    ["SELECT * FROM <tabla>;", "Extraer todos los registros"],
    ["SELECT USER();",         "Ver usuario actual conectado"],
    ["SELECT VERSION();",      "Ver versión del servidor MySQL"],
    ["SHOW GRANTS;",           "Ver privilegios del usuario actual"],
]
story.append(make_table(data4, [CONTENT_W*0.38, CONTENT_W*0.62], S, mono_cols={0}))

# ── 9. Conexión CPTS ─────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("9. Conexión con CPTS y Mercado Laboral", S["h1"]))
story.append(hr())

story.append(Paragraph(
    "Enumeración de servicios de bases de datos está cubierta en <b>Attacking Common Services</b> "
    "del HTB Academy Penetration Tester Path. MySQL, MSSQL y PostgreSQL comparten el mismo "
    "patrón mental: conectar → enumerar esquema → extraer datos → buscar credenciales reutilizables.",
    S["body"]
))

connections = [
    "<b>CPTS Exam:</b> enumeración de servicios de BD es parte estándar del reconocimiento en cualquier red",
    "<b>Progresión natural:</b> Sequel (acceso directo) → Archetype (MSSQL + xp_cmdshell → RCE) → Querier (MSSQL + PowerUpSQL)",
    "<b>Engagement real (Proyecto Cóndor):</b> bases de datos de desarrollo expuestas sin hardening son un hallazgo recurrente en auditorías de infraestructura",
    "<b>Reporte:</b> documentar hallazgo de BD sin auth requiere: evidencia de conexión + datos sensibles expuestos (sin exfiltrar de más) + impacto + remediación específica del motor",
]
for c in connections:
    story.append(Paragraph(f"• {c}", S["bullet"]))

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    "💡  Compara este PDF con el de Appointment (SQLi): ahí la vulnerabilidad estaba en la "
    "lógica de la aplicación web. Acá está en la configuración del servicio de base de datos. "
    "Dos capas distintas de la misma pila — reconocerlas por separado es lo que distingue "
    "un pentest superficial de uno completo.",
    S["tip"]
))

# ── Footer ────────────────────────────────────────────────────────────────────
story.extend(footer_line(S, "Sequel", "2026"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
