
Instalación de Tmux en Shell:
[sudo apt install tmux -y]

Crear una sesión en tmux:
[tmux new -s HTB]
*(Ojo: muévete primero en la terminal a la carpeta donde vas a trabajar para que las ventanas nuevas se abran en esa ruta).*

Prefijo por defecto de los comandos de tmux:
[CTRL + B]

Combinación de teclas para abrir una nueva ventana en tmux:
Prefijo [CTRL + B] + [C]

Cambiar a cada ventana:
Presionar el prefijo [CTRL + B] y luego el número de la ventana, como 0 o 1.

Dividir una ventana verticalmente en paneles:
Presionando el prefijo [CTRL + B] y luego [SHIFT + %]

Dividir en paneles horizontales:
Presionando el prefijo [CTRL + B] y luego [SHIFT + "]

Cambiar entre paneles:
Presionando el prefijo [CTRL + B] y luego las flechas (izquierda/derecha para cambio horizontal, arriba/abajo para cambio vertical). El panel activo queda con borde verde.

OJO! Truco de terminal:
[CTRL + R]: buscar comandos anteriores en el historial de la terminal (búsqueda recursiva).

---

Lo de arriba lo cambié por esto en root ~/.tmux.conf:

Reasignar la tecla de prefijo a Ctrl+A [00:02:26]
(Ventaja: si te metes por SSH a otra máquina con tmux, tu Ctrl+A maneja tu tmux local y Ctrl+B maneja la máquina remota sin conflicto).
set -g prefix C-a
unbind C-b
bind-key C-a send-prefix

Límite del buffer de historial de scroll [00:03:41]
(Por defecto guarda 2000 líneas, aquí lo subes a 10000).
set -g history-limit 10000

Evitar que los títulos de ventana se renombren automáticamente [00:03:56]
set-option -g allow-rename off

Unir y enviar paneles entre ventanas [00:04:23]
bind-key j command-prompt -p "join pane from:" "join-pane -s '%%'"
bind-key s command-prompt -p "send pane to:" "join-pane -t '%%'"

Habilitar navegación estilo Vi en modo copia [00:05:12]
set-window-option -g mode-keys vi

(Para recargar el archivo sin reiniciar tmux: prefijo [CTRL + A] + [:] y escribes source-file ~/.tmux.conf).

---

Sigo con los comandos de tmux:

Comandos desde la terminal (sin tmux):
tmux ls: nombra las sesiones iniciadas en tmux.
tmux attach -t [Nombre del Objetivo]: ingresar a una sesión de tmux desde terminal.
tmux kill-session -t [Nombre]: cerrar y eliminar una sesión.

---

Comandos y atajos dentro de Tmux (con el prefijo cambiado a Ctrl+A):

Manejo de Sesión y Ventanas:
- Salir de una sesión sin cerrarla (Detach): prefijo [CTRL + A] + [D].
  (Tus herramientas y comandos siguen corriendo en segundo plano).
- Abrir una nueva ventana: prefijo [CTRL + A] + [C].
- Cambiar entre ventanas: prefijo [CTRL + A] + [0-9] (el número de la ventana).
- Renombrar la ventana actual: prefijo [CTRL + A] + [,].
- Cerrar la ventana actual: prefijo [CTRL + A] + [&].

Manejo de Paneles (Splits):
- Dividir panel verticalmente (lado a lado): prefijo [CTRL + A] + [SHIFT + %].
- Dividir panel horizontalmente (arriba y abajo): prefijo [CTRL + A] + [SHIFT + "].
- Cambiar entre paneles: prefijo [CTRL + A] y luego las flechas de dirección.
- Zoom en un panel (ponerlo a pantalla completa): prefijo [CTRL + A] + [Z].
  (Presionas lo mismo de nuevo para volver a ver todos los paneles).
- Cambiar el tamaño de los paneles: mantener presionado [CTRL] junto con [A] y usar las flechas del teclado.
- Mover de posición un panel: prefijo [CTRL + A] + [{] para mover a la izquierda o [}] para mover a la derecha.
- Cambiar el diseño/distribución automática de paneles: prefijo [CTRL + A] + [Espacio].
- Cerrar el panel actual: prefijo [CTRL + A] + [X].

Enviar y Traer Paneles entre Ventanas (los atajos 's' y 'j' del .tmux.conf):
- Enviar el panel actual a otra ventana: prefijo [CTRL + A] + [S] y escribes el número de la ventana destino.
- Traer un panel de otra ventana a la actual: prefijo [CTRL + A] + [J] y escribes el número de la ventana origen.

Modo Copia y Búsqueda (estilo Vi):
- Entrar al modo scroll / copia: prefijo [CTRL + A] + [ [ ] (corchete que abre).
  Te puedes mover con flechas, Page Up / Page Down o teclas Vi (h, j, k, l).
- Buscar texto hacia arriba: escribir ?palabra y presionar [ENTER]. Con la tecla 'n' vas a la siguiente coincidencia.
- Buscar texto hacia abajo: escribir /palabra y presionar [ENTER].
- Seleccionar texto: te ubicas al inicio del texto y presionas [Espacio], luego te mueves hasta el final de la selección.
- Copiar la selección: presionas [ENTER] (queda en el búfer de tmux).
- Pegar el texto copiado: prefijo [CTRL + A] + [ ] ] (corchete que cierra).

Plugin de Registro (tmux-logging):
- Guardar todo el historial de la pantalla a un archivo log: prefijo [CTRL + A] + [ALT + SHIFT + P].
  (Útil en auditorías o CTFs para no perder credenciales o salidas de Nmap).

Otros atajos útiles:
- Ver la lista de todos los comandos y atajos: prefijo [CTRL + A] + [?].
- Ver reloj en pantalla: prefijo [CTRL + A] + [T].

---

Trucos de Terminal / Bash del video:
- [CTRL + R]: buscar comandos anteriores en el historial de bash escribiendo palabras clave.
- [ALT + .]: pega el último argumento del comando anterior (si lo presionas varias veces, va retrocediendo en el historial).
- [CTRL + A] presionado dos veces rápido: ir al principio de la línea en bash (al usar Ctrl+A como prefijo de tmux, hay que pulsarlo dos veces para que llegue a bash).
- [CTRL + E]: ir al final de la línea en bash.
- [CTRL + Flechas]: saltar palabra por palabra en la línea de comandos.