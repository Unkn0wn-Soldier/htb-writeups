# 🗺️ Roadmap 2026–2027 — CPTS (fecha recalibrada 2026-09-12)

> [!info] Objetivo principal
> **Certificación CPTS (HTB Certified Penetration Testing Specialist)**.
> Inicio real: junio 2026 · Recalibrado: 12-sep-2026 · Nueva ventana objetivo: **abril–septiembre 2027**.
>
> El CPTS es el objetivo correcto para tu situación actual: usa exactamente el material de HTB Academy, es 100% práctico, y es cada vez más reconocido en el mercado latinoamericano. OSCP+ pasa a 2028 (ver nota al final).

> [!danger] Por qué se movió la fecha (12-sep-2026)
> Formalizaste la inscripción al **Penetration Tester Job Role Path** de HTB Academy (28 módulos, contador oficial de HTB: **44d 2h**). Convertido con la convención real de HTB (1 día = 8h de estudio, confirmado cruzando el contador oficial del path contra el detalle por módulo — ver metodología abajo), son **~354 horas** solo de contenido + assessments del path, que es un **gate obligatorio y no negociable**: no se puede rendir el examen CPTS sin el 100% del path completo, assessments incluidos. Fuente: [HTB Academy — Penetration Tester Path](https://academy.hackthebox.com/path/preview/penetration-tester), [HTB Help Center](https://help.hackthebox.com/en/articles/12741910-academy-modules-paths).
>
> A 1–2h/día (≈7–14h/semana) esas 354h solas ya ocupan entre 25 y 51 semanas. Sumando ~35 máquinas restantes del roadmap original (~140h estimadas) y buffer de repaso/reporting (~35h), el total remanente ronda **~530h**. Diciembre 2026 (110 días desde hoy) solo da 110–220h disponibles en el mejor caso — no alcanza ni para el path solo. La cuenta completa vive en la sección "Metodología de recálculo" al final de este documento.

> [!warning] Sobre suscripciones HTB
> **Free/Student:** Solo máquinas activas + Starting Point (siempre gratis) + Academy con límite de cubes/tiempo según plan Student.
> **VIP (~$14/mes):** Acceso a máquinas retiradas estándar.
> **VIP+:** Acceso a TODO (incluye máquinas antiguas como Lame, Legacy, Blue, etc.).
> → **Estrategia:** Completa Starting Point con Free mientras avanzas el Academy Path en paralelo. Para Fases 1-3 necesitas mínimo VIP.

---

## Resumen del Plan (recalibrado)

| Fase | Periodo (nuevo) | Foco | Meta | Suscripción |
| ---- | ------- | ---- | ---- | ----------- |
| 0 — Starting Point | Jun 2026 – Nov 2026 | Servicios básicos + primeras vulns web | 23 máquinas SP + writeups (Oopsie descartada) | **Free** |
| 1 — Fundamentos + Academy (bloque grande) | Sep 2026 – Mar 2027 | Medium Linux + 19 módulos Academy (fundamentos + web) | 10 máquinas + 19 módulos CPTS | VIP |
| 2 — Active Directory | Mar–May 2027 | Medium Windows / AD | 10 máquinas AD + 4 módulos AD | VIP |
| 3 — Exam Prep | May–Jul 2027 | Hard + simulación examen | 6 máquinas + 5 módulos + Pro Lab opcional | VIP/VIP+ |
| Examen CPTS | Jul–Sep 2027 | 10 días de lab + reporte | CERTIFICACIÓN | — |

Este cronograma asume **~10h/semana promedio sostenido** (punto medio realista de "1-2h/día", sin huecos tipo el de julio 2026). Si sostenés 12-14h/semana sin interrupciones, todo el plan se corre ~2 meses antes (aterrizando en Q2 2027 en vez de Q3). Revisar cada 2 semanas contra el ritmo real, no contra el plan optimista.

---

## Fase 0 — Starting Point: Free Tier (Junio 2026 – Noviembre 2026)

> [!warning] Regla de esta fase
> Sin writeup = la máquina no cuenta. Escribe el writeup ANTES de ver el oficial.
> El Starting Point está ordenado por dificultad creciente — sigue el orden.

El Starting Point cubre exactamente lo que necesitas antes de tocar máquinas retiradas:
servicios expuestos, credenciales por defecto, web básica, privesc, y scripting.
De las 24 máquinas originales, 4 son VIP+ (fuera de alcance en Free) y 1 (Oopsie) fue
descartada el 12-sep-2026 — quedan **23 machines objetivo**, de las cuales ya hiciste 10.

### Tier 0 — Servicios y Credenciales (no requieren scripting)

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 1 | **Meow** ✅ | Telnet · credenciales por defecto | nmap, telnet |
| 2 | **Fawn** ✅ | FTP anónimo | nmap, ftp |
| 3 | **Dancing** ✅ | SMB anónimo · enumeración de shares | nmap, smbclient |
| 4 | **Redeemer** ✅ | Redis sin autenticación | nmap, redis-cli |
| 5 | **Explosion** | 🔒 VIP+ — fuera de alcance en Free | xfreerdp |
| 6 | **Preignition** | 🔒 VIP+ — fuera de alcance en Free | gobuster, curl |
| 7 | **Mongod** | 🔒 VIP+ — fuera de alcance en Free | nmap, mongosh |
| 8 | **Synced** | 🔒 VIP+ — fuera de alcance en Free | nmap, rsync |

### Tier 1 — Web básica + servicios mixtos

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 9 | **Appointment** ✅ | SQL Injection (login bypass) | nmap, curl, burp |
| 10 | **Sequel** ✅ | MySQL sin contraseña | nmap, mysql |
| 11 | **Crocodile** ✅ | FTP anónimo + credenciales web | nmap, ftp, gobuster |
| 12 | **Responder** ✅ | LLMNR/NBT-NS poisoning · NTLMv2 | Responder, hashcat |
| 13 | **Three** ✅ | S3 bucket público · AWS misconfig | nmap, awscli |
| 14 | **Ignition** | Laravel admin · credenciales por defecto | gobuster, curl |
| 15 | **Bike** | SSTI (Node.js / Handlebars) | burp, curl |
| 16 | **Pennyworth** | Jenkins Groovy Script Console · RCE | nmap, curl |
| 17 | **Tactics** | SMB + PsExec · lateral movement | nmap, psexec.py |

### Tier 2 — Cadena de vulnerabilidades

| # | Máquina | Técnica principal | Herramienta clave |
|---|---------|-------------------|-------------------|
| 18 | **Archetype** | MSSQL · xp_cmdshell · PS history | mssqlclient.py, winPEAS |
| 19 | ~~Oopsie~~ | ❌ **Descartada (12-sep-2026)** — IDOR · cookie tampering · upload RCE · PATH hijack en SUID. Cubierta en teoría por los módulos Academy **File Upload Attacks** y **Linux Privilege Escalation** (Fase 1) | — |
| 20 | **Vaccine** ✅ | FTP · SQLi · sudo vi privesc | sqlmap, ftp |
| 21 | **Unified** | Log4Shell (CVE-2021-44228) · UniFi | nmap, rogue-jndi |
| 22 | **Included** | TFTP · LFI · Docker privesc | tftp, curl |
| 23 | **Markup** | XXE · cron job privesc | burp, pspy |
| 24 | **Base** | Insecure comparison (PHP) · sudo cp | burp, sudo -l |

**Meta al terminar Fase 0:** 23 writeups · dominas el flujo nmap→enum→foothold→flags · conoces Burp, smbclient, hashcat, sqlmap, y básicos de web vulns.

> [!tip] Nota sobre Oopsie
> El PATH hijacking sobre binario SUID (la técnica específica y menos común de Oopsie, distinta de GTFOBins) no queda cubierta 1:1 por ningún módulo Academy garantizado. Si en Fase 1 el módulo **Linux Privilege Escalation** no la toca explícitamente, vale la pena volver a esta máquina como práctica puntual antes del examen — no es urgente, pero quedó anotado para no perder la técnica.

---

## Fase 1 — Fundamentos Linux + Web + HTB Academy (Septiembre 2026 – Marzo 2027)

> [!note] Requiere VIP (~$14/mes) para las máquinas retiradas de esta fase. Evalúa upgradear ahora que el Academy Path es la prioridad.

Este es el bloque más largo del roadmap recalibrado: concentra los **19 módulos** del
Academy Path que cubren fundamentos de metodología, Linux y vulnerabilidades web —
exactamente el terreno que ya conocés por las máquinas de Fase 0, ahora formalizado
con la profundidad y los assessments que pide el examen. En paralelo, seguís sumando
máquinas Medium Linux retiradas.

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

### Módulos HTB Academy a completar en Fase 1 (19 — lista completa, antes faltaban 10)

**Metodología y fundamentos:**
- [ ] Penetration Testing Process — 6h
- [ ] Getting Started — 1d
- [ ] Network Enumeration with Nmap — 7h
- [ ] Footprinting — 2d
- [ ] Information Gathering - Web Edition — 1d
- [ ] Vulnerability Assessment — 2h
- [ ] File Transfers — 3h
- [ ] Shells & Payloads — 2d
- [ ] Using the Metasploit Framework — 5h
- [ ] Password Attacks — 3d
- [ ] Linux Privilege Escalation — 1d

**Web (agregados el 12-sep-2026 — antes no estaban en ninguna fase):**
- [ ] SQL Injection Fundamentals — 1d
- [ ] SQLMap Essentials — 4h
- [ ] Cross-Site Scripting (XSS) — 6h
- [ ] File Inclusion — 1d
- [ ] File Upload Attacks — 1d *(reemplaza la práctica de Oopsie)*
- [ ] Command Injections — 6h
- [ ] Attacking Web Applications with Ffuf — 5h
- [ ] Login Brute Forcing — 6h

Subtotal Fase 1: **~154 horas** de contenido Academy (de las 354h totales del path).

---

## Fase 2 — Active Directory (Marzo – Mayo 2027)

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

### Módulos HTB Academy a completar en Fase 2 (4 — sin cambios)

- [ ] Active Directory Enumeration & Attacks — 7d
- [ ] Attacking Common Services — 1d
- [ ] Pivoting, Tunneling, and Port Forwarding — 2d
- [ ] Using Web Proxies — 1d

Subtotal Fase 2: **~88 horas** de contenido Academy.

---

## Fase 3 — Exam Prep (Mayo – Julio 2027)

> [!note] Requiere VIP. Las máquinas más antiguas (Arctic, Bastard) pueden requerir VIP+.

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 45 | **Poison** | FreeBSD | LFI → log poisoning → RCE |
| 46 | **Bastard** | Windows | Drupal RCE (Druplion), MS15-051 |
| 47 | **Bounty** | Windows | IIS upload bypass (.config → RCE) |
| 48 | **Chatterbox** | Windows | AChat buffer overflow, AutoLogon creds |
| 49 | **Arctic** | Windows | ColdFusion 8 file upload |
| 50 | **Bank** | Linux | DNS spoofing, SQLi, bypass extensión |

### Módulos HTB Academy a completar en Fase 3 (5 — sin cambios)

- [ ] Web Attacks — 2d
- [ ] Attacking Common Applications — 4d
- [ ] Windows Privilege Escalation — 4d
- [ ] Documentation & Reporting — 2d
- [ ] Attacking Enterprise Networks — 2d

Subtotal Fase 3: **~112 horas** de contenido Academy.

> [!tip] Pro Lab opcional
> El **Pro Lab Dante** (HTB) es el más cercano al examen CPTS. Red completa con múltiples máquinas y pivoting. Si no tienes presupuesto/tiempo, las 49 máquinas de este roadmap son suficientes.

---

## Examen CPTS — Julio / Septiembre 2027

> [!danger] Checklist pre-examen (NO compres el voucher hasta cumplir esto)
> - [ ] Completaste el 100% de los 28 módulos del Penetration Tester Path en HTB Academy, **incluyendo todos los skill assessments** (gate obligatorio confirmado — no hay compra de examen sin esto)
> - [ ] Tienes 35+ máquinas de este roadmap resueltas con writeup
> - [ ] Puedes hacer Kerberoasting y AS-REP Roasting de memoria
> - [ ] Puedes escribir un reporte de pentest profesional en menos de 4 horas
> - [ ] Completaste al menos una máquina Hard sin ver hints

El examen dura **10 días** de lab activo + **2 días** para entregar el reporte. Es una red corporativa completa. **El reporte es tan importante como los flags** — si el reporte está mal, repruebas aunque hayas rooteado todo. Esos 12 días son intensivos y no entran en el presupuesto de 1-2h/día — bloquéalos como vacaciones/tiempo dedicado cuando se acerque la fecha.

**Costo:** ~USD $210 (voucher) + $14/mes HTB Student que ya pagas.

---

## Metodología de recálculo del ritmo (12-sep-2026)

Cifras y fuente de cada una, para poder auditar este cronograma más adelante:

| Concepto | Cifra | Fuente / cómo se calculó |
| --- | --- | --- |
| Total Academy Path (contador HTB) | 44d 2h | Pantalla de "Path Progress" de César, 12-sep-2026 |
| Conversión d→h | 1d = 8h | Confirmado cruzando 44d2h (=354h) contra la suma manual de las 28 duraciones individuales por módulo (154+88+112=354h exacto) y contra estimación independiente de ~342h reportada por fuentes externas para el mismo path |
| Horas totales Academy Path | ~354h | 44×8+2 = 354, más suma módulo por módulo (ver fases arriba) |
| Gate obligatorio 100% + assessments | Confirmado | [HTB Academy — Penetration Tester Path](https://academy.hackthebox.com/path/preview/penetration-tester) · [HTB Help Center](https://help.hackthebox.com/en/articles/12741910-academy-modules-paths) · [CertCrush — study plan CPTS 2026](https://www.certcrush.app/blog/how-to-pass-htb-cpts-2026-study-plan-10-day-practical) |
| Máquinas restantes estimadas (~35) | ~140h | Estimación propia — NO es dato oficial. Basado en tu ritmo reciente real (Vaccine: ~2h; ritmo Ago 2026: 4 máquinas en 12 días) con buffer mayor para AD/Windows (Fase 2-3), que suelen tomar más que Linux fácil |
| Buffer repaso/reporting | ~35h | Estimación propia, colchón para repasar Técnicas/ y practicar reportes antes del examen |
| **Total remanente** | **~530h** | Academy (354h) + máquinas (~140h) + buffer (~35h) |
| Ventana a 10h/semana | ~53 semanas ≈ 12 meses | 530/10 — escenario conservador y sostenible |
| Ventana a 12-14h/semana | ~38-44 semanas ≈ 9-10 meses | 530/12 a 530/14 — escenario ambicioso, exige cero huecos tipo julio 2026 |

**Nivel de confianza:** Alto en el gate del 100% y en las 354h del path (dos fuentes independientes + verificación aritmética propia). Medio-bajo en las ~140h de máquinas restantes y el buffer (son estimación mía, no dato de HTB) — ajustar estas dos filas a medida que completes Fase 1 y tengas datos reales de tiempo por máquina Medium/AD.

---

## Post-CPTS — Hoja de Ruta 2028

CPTS + título en Ciberseguridad (2027) = perfil competitivo para pentesting en Chile. Siguiente paso: **OSCP+** (OffSec) pasa de 2027 a 2028 por el corrimiento de este roadmap — revisar cuando el CPTS esté rendido, no antes.