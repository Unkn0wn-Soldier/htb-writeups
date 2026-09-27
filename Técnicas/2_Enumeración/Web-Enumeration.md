---
tags:
  - tecnica
  - categoria/discovery
  - os/agnostic
  - nivel/basico
fecha_aprendida: 2026-09-26
fuente: HTB Academy - Network Enumeration with Nmap
mitre_technique: T1595.002
---
# ⚔️ Web Enumeration

> [!abstract] Resumen
> Enumeración activa de servidores web (80/443) para descubrir directorios, archivos, subdominios, tecnologías y datos filtrados en fuentes accesorias (robots.txt, certificados, código fuente). Alta superficie de ataque cuando la organización tiene pocos servicios expuestos.

---

## ¿Qué es y por qué funciona?

Un servidor web suele exponer más de lo que el desarrollador pretende: instalaciones sin terminar (WordPress en modo setup), archivos de config con permisos débiles, paneles de admin no enlazados desde el sitio público, o comentarios de desarrollo dejados en el HTML. Nada de esto requiere explotar una vulnerabilidad — solo pedir la URL correcta. El fuzzing de directorios/subdominios y la revisión manual de fuentes secundarias (robots.txt, certificados TLS, cabeceras, código fuente) cubren la mayoría de estos hallazgos.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Puerto 80/443 (u otro HTTP/S) accesible
> - Wordlist adecuada al contexto (common.txt para dirs genéricos, namelist.txt para DNS)
> - Para DNS brute-force: resolver configurado (`/etc/resolv.conf`) apuntando a un DNS público (1.1.1.1) si el objetivo no está en un DNS interno

---

## Procedimiento

### Enumeración de directorios/archivos

```bash
gobuster dir -u http://<IP>/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
# Códigos clave: 200 (existe), 301/302 (redirect, no es fallo), 403 (prohibido, existe pero sin acceso)
```

### Enumeración de subdominios DNS

```bash
gobuster dns -d <dominio> -w /usr/share/SecLists/Discovery/DNS/namelist.txt
```

### Banner grabbing / cabeceras HTTP

```bash
curl -IL https://<host>
# Revela: framework, versión de servidor, headers de seguridad faltantes
```

### Fingerprinting de tecnología

```bash
whatweb <IP>
whatweb --no-errors <IP>/24    # barrido de subred completa
```

### Fuentes secundarias (manual)

| Fuente | Qué buscar |
|---|---|
| `robots.txt` | Rutas `Disallow` — suelen ser justo lo que quieren ocultar (`/private`, `/admin`) |
| Certificado TLS | CN/SAN, email, org — útil para phishing si está en alcance |
| Código fuente (Ctrl+U) | Comentarios de dev con credenciales, endpoints ocultos, versiones de librerías |

> [!tip] Variaciones comunes
> - Si `dir` mode no encuentra nada, probar extensiones específicas: `-x php,txt,bak`
> - Un 403 en gobuster no significa "descartar" — puede ser bypasseable (headers, trailing slash, encoding)
> - WordPress en modo setup (`/wp-admin/setup-config.php` accesible) = RCE casi garantizado vía tema/plugin editor una vez completada la instalación

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| gobuster | Fuzzing de dirs/dns/vhost | `gobuster dir -u <url> -w <wordlist>` |
| ffuf | Fuzzing más flexible (params, headers) | `ffuf -u <url>/FUZZ -w <wordlist>` |
| whatweb | Fingerprinting de stack tecnológico | `whatweb <IP>` |
| curl | Inspección manual de headers/respuestas | `curl -IL <url>` |
| EyeWitness | Screenshots + fingerprint masivo | `eyewitness --web -f urls.txt` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Eliminar instalaciones default/incompletas antes de exponer a producción. `robots.txt` no es control de acceso — cualquier ruta sensible ahí debe además tener autenticación real. Headers de seguridad (`Server`, `X-Powered-By`) minimizados u ofuscados para reducir fingerprinting. Revisión de código antes de deploy para eliminar comentarios con credenciales.

---

## Dónde la usé

- HTB Academy — Network Enumeration with Nmap, sección Web Enumeration (2026-09-26)

---

## Referencias

- [HackTricks - Web Enumeration](https://book.hacktricks.xyz/pentesting-web)
- [MITRE ATT&CK - T1595.002](https://attack.mitre.org/techniques/T1595/002/)
