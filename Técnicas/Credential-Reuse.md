---
tags:
  - tecnica
  - categoria/initial-access
  - categoria/credential-access
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-08-13
fuente: HTB/Crocodile
mitre_technique: T1078
---
# ⚔️ Credential Reuse (Cross-Service)

> [!abstract] Resumen
> Credenciales obtenidas de un servicio sin autenticación (o mal protegido) se reutilizan para autenticar en un segundo servicio distinto. El primer servicio no es el objetivo — es el punto de apoyo.

---

## ¿Qué es y por qué funciona?

Es común que administradores o desarrolladores dejen credenciales de un sistema accesibles en otro — archivos de configuración, backups, listados de usuarios en un share o FTP sin auth, notas internas expuestas. Funciona porque los humanos reutilizan contraseñas entre sistemas por comodidad, y porque el primer servicio comprometido rara vez se trata como "crítico" (es solo un FTP, solo un share) cuando en realidad es la llave de otro sistema que sí lo es.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Un servicio accesible sin autenticación fuerte (FTP anónimo, SMB null session, share mal permisado, repo público, etc.)
> - Ese servicio expone, directa o indirectamente, credenciales (archivos de texto, configs, backups, hashes)
> - Un segundo servicio (login web, SSH, otro panel) que acepta esas mismas credenciales

---

## Procedimiento

### Detección / Enumeración

```bash
# Cualquier servicio sin auth es candidato — enumerar su contenido completo
# antes de descartarlo, buscando patrones de credenciales:
ftp <IP>       # o smbclient, o revisar un repo/backup expuesto
ftp> ls -la
ftp> get <cualquier_archivo_de_texto>

cat <archivo>
# Buscar: user/username/login, pass/password/pwd, patrones tipo "usuario:clave"
```

### Explotación

```bash
# Paso 1: extraer todo archivo de texto del servicio sin auth
# Paso 2: identificar el segundo servicio (enumeración web, puertos, etc.)
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt

# Paso 3: probar las credenciales extraídas en el login encontrado
# Manual (formulario) o con Hydra/Burp Intruder si hay varias combinaciones
```

> [!tip] Variaciones comunes
> - Credenciales en dos archivos separados (usuarios en uno, contraseñas en otro) — no asumir que vienen juntas
> - El servicio origen puede ser cualquiera con acceso a archivos: FTP anónimo, SMB null session, S3 bucket público, repo Git expuesto
> - Si hay múltiples usuarios y una sola contraseña (o viceversa), probar combinaciones — puede ser password spray encubierto

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| ftp / smbclient | Extraer archivos del servicio origen | `ftp <IP>` / `smbclient //<IP>/<share> -N` |
| gobuster | Encontrar el segundo servicio (panel de login) | `gobuster dir -u http://<IP>/ -w wordlist.txt` |
| Hydra | Probar combinaciones si hay varias credenciales candidatas | `hydra -L users.txt -P pass.txt <IP> http-post-form "..."` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Nunca almacenar credenciales en texto plano en ubicaciones accesibles sin autenticación fuerte. Contraseñas únicas por servicio (gestor de contraseñas / secretos, no reutilización manual). Auditar periódicamente qué archivos son accesibles vía servicios sin auth (FTP anónimo, shares abiertos). Correlacionar en SIEM accesos a distintos servicios desde la misma IP en ventanas de tiempo cortas.

---

## Dónde la usé

- `[[HTB/Crocodile/Crocodile]]` — Credenciales extraídas de FTP anónimo (`allowed.userlist` / `allowed.userlist.passwd`), reutilizadas en `/login.php`

---

## Referencias

- [HackTricks - FTP](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ftp)
- [MITRE ATT&CK - T1078](https://attack.mitre.org/techniques/T1078/)
