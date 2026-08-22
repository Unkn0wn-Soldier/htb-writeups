---
tags:
  - tecnica
  - categoria/initial-access
  - os/linux
  - os/windows
  - nivel/basico
fecha_aprendida: 2026-06-05
fuente: HTB/Meow
mitre_technique: T1078.001
---
# ⚔️ Default / Empty Credentials

> [!abstract] Resumen
> Acceso a un servicio remoto usando credenciales por defecto del fabricante, o una cuenta administrativa sin contraseña configurada. No requiere exploit — es un error de configuración/despliegue.

---

## ¿Qué es y por qué funciona?

Muchos servicios (Telnet, FTP, RDP, paneles web, dispositivos IoT) se despliegan con una cuenta administrativa preconfigurada (`root`, `admin`) sin contraseña, o con una contraseña documentada públicamente por el fabricante. Si el operador no la cambia post-instalación, cualquiera con acceso de red al servicio puede autenticarse directamente. Funciona porque el servicio no distingue entre "administrador legítimo que nunca cambió la clave" y "atacante que la conoce" — la autenticación es válida en ambos casos.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - El servicio de autenticación remota debe estar expuesto y accesible (puerto abierto)
> - El operador no cambió la credencial por defecto tras el despliegue
> - No hay bloqueo por intentos fallidos ni rate limiting activo (facilita probar varias combinaciones)

---

## Procedimiento

### Detección / Enumeración

```bash
# Identificar el servicio y su naturaleza vía nmap
nmap -sCV -p- --min-rate 5000 <IP>

# Buscar en la salida: versión del servicio, banner, título de panel web
# → identifica el fabricante/producto para buscar sus defaults conocidos
```

### Explotación

```bash
# Paso 1: identificar el servicio (Telnet, FTP, RDP, panel admin, etc.)

# Paso 2: probar credenciales en orden de probabilidad
# Linux: root (sin pass) → admin → user → guest
# Windows/paneles: admin/admin → admin/password → guest/guest

telnet <IP>
# login: root
# password: (Enter vacío)

# Paso 3: si falla, consultar cheat sheet de credenciales por defecto
```

> [!tip] Variaciones comunes
> - Telnet/SSH: `root` sin contraseña (Meow)
> - FTP: usuario `anonymous`, cualquier contraseña o vacía (Fawn — técnicamente distinto, ver [[Ftp-Anonymous]] si se crea)
> - RDP/paneles web: buscar el producto exacto en [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| telnet | Cliente Telnet | `telnet <IP>` |
| hydra | Fuerza bruta de credenciales si defaults simples fallan | `hydra -l root -P wordlist <IP> telnet` |
| DefaultCreds-Cheat-Sheet | Base de datos de credenciales por defecto por producto | — (repo GitHub) |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Rotar toda credencial por defecto en el proceso de despliegue (hardening checklist). Forzar cambio de contraseña en primer login. Deshabilitar cuentas administrativas remotas no usadas. Implementar lockout tras N intentos fallidos y alertar en SIEM ante logins exitosos desde IPs no corporativas en cuentas privilegiadas.

---

## Dónde la usé

- `[[HTB/Meow/Meow]]` — Telnet, `root` sin contraseña, shell root directa
- `[[HTB/Fawn/Fawn]]` — FTP anonymous login (variante: cuenta pública, no credencial filtrada)

---

## Referencias

- [HackTricks - Default Credentials](https://book.hacktricks.xyz/)
- [MITRE ATT&CK - T1078.001](https://attack.mitre.org/techniques/T1078/001/)
- [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)
