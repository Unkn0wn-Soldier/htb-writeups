# 🗺️ Roadmap 2026 — CPTS antes de Diciembre

> [!info] Objetivo principal
> **Certificación CPTS (HTB Certified Penetration Testing Specialist)** antes de diciembre 2026.
> Inicio: junio 2026 · Duración disponible: ~6 meses.
>
> El CPTS es el objetivo correcto para tu situación actual: usa exactamente el material de HTB Academy, es 100% práctico, y es cada vez más reconocido en el mercado latinoamericano. OSCP+ es el paso lógico en 2027.

> [!warning] Sobre suscripciones HTB
> **Free/Student:** Solo máquinas activas + Starting Point (siempre gratis).
> **VIP (~$14/mes):** Acceso a máquinas retiradas estándar.
> **VIP+:** Acceso a TODO (incluye máquinas antiguas como Lame, Legacy, Blue, etc.).
> → **Estrategia:** Completa Starting Point con Free. Para Fases 1-3 necesitas mínimo VIP.

---

## Resumen del Plan

| Fase | Periodo | Foco | Meta | Suscripción |
| ---- | ------- | ---- | ---- | ----------- |
| 0 — Starting Point | Jun–Jul 2026 | Servicios básicos + primeras vulns web | 24 máquinas SP + writeups | **Free** |
| 1 — Fundamentos | Jul–Sep 2026 | Medium Linux + HTB Academy | 15 máquinas + módulos CPTS | VIP |
| 2 — Active Directory | Sep–Oct 2026 | Medium Windows / AD | 10 máquinas AD + módulos AD | VIP |
| 3 — Exam Prep | Oct–Nov 2026 | Hard + simulación examen | 5 máquinas Hard + Pro Lab | VIP/VIP+ |
| Examen CPTS | Nov–Dic 2026 | 10 días de lab + reporte | CERTIFICACIÓN | — |

---

## Fase 0 — Starting Point: Free Tier (Junio – Julio 2026)

> [!warning] Regla de esta fase
> Sin writeup = la máquina no cuenta. Escribe el writeup ANTES de ver el oficial.
> El Starting Point está ordenado por dificultad creciente — sigue el orden.

El Starting Point cubre exactamente lo que necesitas antes de tocar máquinas retiradas:
servicios expuestos, credenciales por defecto, web básica, privesc, y scripting.
Son 24 máquinas 100% gratuitas, estructuradas en 3 tiers.

### Tier 0 — Servicios y Credenciales (no requieren scripting)

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 1 | **Meow** ✅ | Telnet · credenciales por defecto | nmap, telnet |
| 2 | **Fawn** | FTP anónimo | nmap, ftp |
| 3 | **Dancing** | SMB anónimo · enumeración de shares | nmap, smbclient |
| 4 | **Redeemer** | Redis sin autenticación | nmap, redis-cli |
| 5 | **Explosion** | RDP · credenciales por defecto | nmap, xfreerdp |
| 6 | **Preignition** | Web · panel admin · gobuster | gobuster, curl |
| 7 | **Mongod** | MongoDB sin autenticación | nmap, mongosh |
| 8 | **Synced** | rsync anónimo | nmap, rsync |

### Tier 1 — Web básica + servicios mixtos

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 9 | **Appointment** | SQL Injection (login bypass) | nmap, curl, burp |
| 10 | **Sequel** | MySQL sin contraseña | nmap, mysql |
| 11 | **Crocodile** | FTP anónimo + credenciales web | nmap, ftp, gobuster |
| 12 | **Responder** | LLMNR/NBT-NS poisoning · NTLMv2 | Responder, hashcat |
| 13 | **Three** | S3 bucket público · AWS misconfig | nmap, awscli |
| 14 | **Ignition** | Laravel admin · credenciales por defecto | gobuster, curl |
| 15 | **Bike** | SSTI (Node.js / Handlebars) | burp, curl |
| 16 | **Pennyworth** | Jenkins Groovy Script Console · RCE | nmap, curl |
| 17 | **Tactics** | SMB + PsExec · lateral movement | nmap, psexec.py |

### Tier 2 — Cadena de vulnerabilidades

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 18 | **Archetype** | MSSQL · xp_cmdshell · PS history | mssqlclient.py, winPEAS |
| 19 | **Oopsie** | IDOR · upload bypass · SUID privesc | burp, find |
| 20 | **Vaccine** | FTP · SQLi · sudo vi privesc | sqlmap, ftp |
| 21 | **Unified** | Log4Shell (CVE-2021-44228) · UniFi | nmap, rogue-jndi |
| 22 | **Included** | TFTP · LFI · Docker privesc | tftp, curl |
| 23 | **Markup** | XXE · cron job privesc | burp, pspy |
| 24 | **Base** | Insecure comparison (PHP) · sudo cp | burp, sudo -l |

**Meta al terminar Fase 0:** 24 writeups · dominas el flujo nmap→enum→foothold→flags · conoces Burp, smbclient, hashcat, sqlmap, y básicos de web vulns.

---

## Fase 1 — Fundamentos Linux + HTB Academy (Julio – Septiembre 2026)

> [!note] Requiere VIP (~$14/mes). Evalúa upgradear cuando termines Fase 0.

En paralelo con las máquinas, avanza en los módulos del **Penetration Tester Job Role Path** de HTB Academy. Ese path es exactamente lo que cubre el examen CPTS.

### Máquinas de Fase 1 (Medium Linux, retiradas — requieren VIP)

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 25 | **Valentine** | Linux | Heartbleed (CVE-2014-0160), RSA privkey |
| 26 | **Networked** | Linux | PHP file upload bypass, cron privesc |
| 27 | **SwagShop** | Linux | Magento SQLi + RCE, sudo vi |
| 28 | **Postman** | Linux | Redis unauthorized access, webmin |
| 29 | **OpenAdmin** | Linux | OpenNetAdmin RCE, SSH key loot |
| 30 | **Tabby** | Linux | Tomcat LFI + WAR deploy, zip password |
| 31 | **Doctor** | Linux | SSTI (Server-Side Template Injection) |
| 32 | **Magic** | Linux | File upload bypass (doble extensión), SQLi |
| 33 | **TartarSauce** | Linux | Monstra CMS, plugin RFI, sudo tar |
| 34 | **Mango** | Linux | NoSQL injection (MongoDB), sudo jjs |

### Módulos HTB Academy a completar en Fase 1

- [ ] Network Enumeration with Nmap
- [ ] Footprinting
- [ ] Information Gathering - Web Edition
- [ ] Vulnerability Assessment
- [ ] File Transfers
- [ ] Shells & Payloads
- [ ] Using the Metasploit Framework
- [ ] Password Attacks
- [ ] Linux Privilege Escalation

---

## Fase 2 — Active Directory (Septiembre – Octubre 2026)

> [!note] Requiere VIP. Algunas máquinas más antiguas pueden requerir VIP+.

El examen CPTS tiene un componente importante de Active Directory.

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 35 | **Return** | Windows | Printer abuse (credential capture) |
| 36 | **Sauna** | Windows | AS-REP Roasting, DCSync |
| 37 | **Active** | Windows | GPP password, Kerberoasting |
| 38 | **Forest** | Windows | AS-REP Roasting, Exchange privesc, DCSync |
| 39 | **Resolute** | Windows | RPC enum, password spray, DnsAdmin abuse |
| 40 | **Monteverde** | Windows | Azure AD, password spray, Azure blob |
| 41 | **Remote** | Windows | NFS, Umbraco CMS RCE, PS history |
| 42 | **Cascade** | Windows | LDAP enum, AD recycle bin, AES decrypt |
| 43 | **Querier** | Windows | MSSQL, PowerUpSQL, impersonation |
| 44 | **Blackfield** | Windows | AS-REP Roasting, privilege escalation AD avanzada |

### Módulos HTB Academy a completar en Fase 2

- [ ] Active Directory Enumeration & Attacks
- [ ] Attacking Common Services
- [ ] Pivoting, Tunneling, and Port Forwarding
- [ ] Using Web Proxies

---

## Fase 3 — Exam Prep (Octubre – Noviembre 2026)

> [!note] Requiere VIP. Las máquinas más antiguas (Arctic, Bastard) pueden requerir VIP+.

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 45 | **Poison** | FreeBSD | LFI → log poisoning → RCE |
| 46 | **Bastard** | Windows | Drupal RCE (Druplion), MS15-051 |
| 47 | **Bounty** | Windows | IIS upload bypass (.config → RCE) |
| 48 | **Chatterbox** | Windows | AChat buffer overflow, AutoLogon creds |
| 49 | **Arctic** | Windows | ColdFusion 8 file upload |
| 50 | **Bank** | Linux | DNS spoofing, SQLi, bypass extensión |

### Módulos HTB Academy a completar en Fase 3

- [ ] Web Attacks
- [ ] Attacking Common Applications
- [ ] Windows Privilege Escalation
- [ ] Documentation & Reporting
- [ ] Attacking Enterprise Networks

> [!tip] Pro Lab opcional
> El **Pro Lab Dante** (HTB) es el más cercano al examen CPTS. Red completa con múltiples máquinas y pivoting. Si no tienes presupuesto, las 50 máquinas de este roadmap son suficientes.

---

## Examen CPTS — Noviembre / Diciembre 2026

> [!danger] Checklist pre-examen (NO compres el voucher hasta cumplir esto)
> - [ ] Completaste los 28 módulos del Penetration Tester Path en HTB Academy
> - [ ] Tienes 40+ máquinas de este roadmap resueltas con writeup
> - [ ] Puedes hacer Kerberoasting y AS-REP Roasting de memoria
> - [ ] Puedes escribir un reporte de pentest profesional en menos de 4 horas
> - [ ] Completaste al menos una máquina Hard sin ver hints

El examen dura **10 días** de lab activo + **2 días** para entregar el reporte. Es una red corporativa completa. **El reporte es tan importante como los flags** — si el reporte está mal, repruebas aunque hayas rooteado todo.

**Costo:** ~USD $210 (voucher) + $14/mes HTB Student que ya pagas.

---

## Post-CPTS — Hoja de Ruta 2027

CPTS + título en Ciberseguridad (2027) = perfil competitivo para pentesting en Chile. Siguiente paso: **OSCP+** (OffSec), que abre mercado internacional.

En paralelo, **Proyecto Cóndor** puede evolucionar a una propuesta concreta de Red Team as a Service para el mercado chileno: reporting en español, integración normativa local (NCG 461, ISO 27001), y automatización con IA.
