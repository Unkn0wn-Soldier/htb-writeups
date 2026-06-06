# 🗺️ Roadmap 2026 — CPTS antes de Diciembre

> [!info] Objetivo principal
> **Certificación CPTS (HTB Certified Penetration Testing Specialist)** antes de diciembre 2026.
> Inicio: junio 2026 · Duración disponible: ~6 meses.
>
> El CPTS es el objetivo correcto para tu situación actual porque ya tienes HTB Student (el examen usa el mismo material de HTB Academy), es completamente práctico (sin preguntas teóricas), cuesta menos que OSCP+, y es cada vez más reconocido en el mercado latinoamericano. OSCP+ es el paso lógico en 2027.

---

## Resumen del Plan

| Fase | Periodo | Foco | Meta |
| ---- | ------- | ---- | ---- |
| 0 — Baseline | Jun–Jul 2026 | Máquinas Easy retiradas | 10 máquinas + writeups |
| 1 — Fundamentos | Jul–Sep 2026 | Medium Linux + HTB Academy | 15 máquinas + módulos CPTS |
| 2 — Active Directory | Sep–Oct 2026 | Medium Windows / AD | 10 máquinas AD + módulos AD |
| 3 — Exam Prep | Oct–Nov 2026 | Hard + simulación examen | 5 máquinas Hard + Pro Lab |
| Examen CPTS | Nov–Dic 2026 | 10 días de lab + reporte | CERTIFICACIÓN |

---

## Fase 0 — Baseline (Junio – Julio 2026)

> [!warning] Regla de esta fase
> Sin writeup = la máquina no cuenta. Escribe el writeup ANTES de ver el oficial.

Estas 10 máquinas son el punto de partida. Cubren los vectores más frecuentes en cualquier examen práctico. Están ordenadas de menor a mayor complejidad.

| #   | Máquina     | OS      | Dificultad | Técnica principal                     |
| --- | ----------- | ------- | ---------- | ------------------------------------- |
| 1   | **Lame**    | Linux   | Easy       | SMB Samba 3.x exploit (CVE-2007-2447) |
| 2   | **Legacy**  | Windows | Easy       | MS08-067 (NetAPI), SMB                |
| 3   | **Blue**    | Windows | Easy       | EternalBlue MS17-010                  |
| 4   | **Shocker** | Linux   | Easy       | Shellshock (CGI bash)                 |
| 5   | **Bashed**  | Linux   | Easy       | Web shell expuesta, sudo              |
| 6   | **Nibbles** | Linux   | Easy       | Nibbleblog CMS, file upload           |
| 7   | **Devel**   | Windows | Easy       | IIS FTP anónimo + Meterpreter         |
| 8   | **Optimum** | Windows | Easy       | HFS exploit, Sherlock (privesc)       |
| 9   | **Jerry**   | Windows | Easy       | Apache Tomcat manager, WAR deploy     |
| 10  | **Beep**    | Linux   | Easy       | Elastix/FreePBX LFI → RCE             |

**Meta al terminar Fase 0:** 10 writeups en Obsidian · 10 writeups en GitHub · conoces el flujo nmap→foothold→privesc en modo automático.

---

## Fase 1 — Fundamentos Linux + HTB Academy (Julio – Septiembre 2026)

En paralelo con las máquinas, avanza en los módulos del **Penetration Tester Job Role Path** de HTB Academy. Ese path es exactamente lo que cubre el examen CPTS.

### Máquinas de Fase 1 (Medium Linux)

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 11 | **Valentine** | Linux | Heartbleed (CVE-2014-0160), RSA privkey |
| 12 | **Networked** | Linux | PHP file upload bypass, cron privesc |
| 13 | **SwagShop** | Linux | Magento SQLi + RCE, sudo vi |
| 14 | **Postman** | Linux | Redis unauthorized access, webmin |
| 15 | **OpenAdmin** | Linux | OpenNetAdmin RCE, SSH key loot |
| 16 | **Tabby** | Linux | Tomcat LFI + WAR deploy, zip password |
| 17 | **Doctor** | Linux | SSTI (Server-Side Template Injection) |
| 18 | **Magic** | Linux | File upload bypass (doble extensión), SQLi |
| 19 | **TartarSauce** | Linux | Monstra CMS, plugin RFI, sudo tar |
| 20 | **Mango** | Linux | NoSQL injection (MongoDB), sudo jjs |

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

El examen CPTS tiene un componente importante de Active Directory. Esta fase está dedicada exclusivamente a entornos Windows y AD. Las máquinas están ordenadas del vector más simple al más complejo.

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 21 | **Return** | Windows | Printer abuse (credential capture) |
| 22 | **Sauna** | Windows | AS-REP Roasting, DCSync |
| 23 | **Active** | Windows | GPP password, Kerberoasting |
| 24 | **Forest** | Windows | AS-REP Roasting, Exchange privesc, DCSync |
| 25 | **Resolute** | Windows | RPC enum, password spray, DnsAdmin abuse |
| 26 | **Monteverde** | Windows | Azure AD, password spray, Azure blob |
| 27 | **Remote** | Windows | NFS, Umbraco CMS RCE, PS history |
| 28 | **Cascade** | Windows | LDAP enum, AD recycle bin, AES decrypt |
| 29 | **Querier** | Windows | MSSQL, PowerUpSQL, impersonation |
| 30 | **Blackfield** | Windows | AS-REP Roasting, privilege escalation AD avanzada |

### Módulos HTB Academy a completar en Fase 2

- [ ] Active Directory Enumeration & Attacks
- [ ] Attacking Common Services
- [ ] Pivoting, Tunneling, and Port Forwarding
- [ ] Using Web Proxies

---

## Fase 3 — Exam Prep (Octubre – Noviembre 2026)

Esta fase es de endurecimiento. Las máquinas Hard te obligarán a encadenar vulnerabilidades sin pistas evidentes — exactamente como el examen.

| # | Máquina | OS | Técnica principal |
|---|---------|-----|-------------------|
| 31 | **Poison** | FreeBSD | LFI → log poisoning → RCE |
| 32 | **Bastard** | Windows | Drupal RCE (Druplion), MS15-051 |
| 33 | **Bounty** | Windows | IIS upload bypass (.config → RCE) |
| 34 | **Chatterbox** | Windows | AChat buffer overflow, AutoLogon creds |
| 35 | **Arctic** | Windows | ColdFusion 8 file upload |
| 36 | **Bank** | Linux | DNS spoofing, SQLi, bypass extensión |
| 37 | **Admirer** | Linux | Adminer SQLi, credential reuse |
| 38 | **Sunday** | Linux/BSD | Finger, sudo wget con NOPASSWD |
| 39 | **Granny** | Windows | WebDAV upload → ASP shell |
| 40 | **Grandpa** | Windows | IIS 6.0 RCE (CVE-2017-7269) |

### Módulos HTB Academy a completar en Fase 3

- [ ] Web Attacks
- [ ] Attacking Common Applications
- [ ] Windows Privilege Escalation
- [ ] Documentation & Reporting
- [ ] Attacking Enterprise Networks

> [!tip] Pro Lab opcional
> Si tienes presupuesto, el **Pro Lab Dante** (HTB) es el más cercano al examen CPTS. Es una red completa con múltiples máquinas y pivoting. Si no, las 40 máquinas de este roadmap son suficientes.

---

## Examen CPTS — Noviembre / Diciembre 2026

> [!danger] Antes de comprar el voucher del examen, verifica:
> - [ ] Completaste los 28 módulos del Penetration Tester Path en HTB Academy
> - [ ] Tienes 35+ máquinas de este roadmap resueltas con writeup
> - [ ] Puedes hacer Kerberoasting y AS-REP Roasting de memoria
> - [ ] Sabes escribir un reporte de pentest profesional

El examen CPTS dura **10 días** (lab activo), más **2 días** adicionales para entregar el reporte final. Es completamente práctico: una red corporativa que debes comprometer y documentar. El reporte es tan importante como los flags — si el reporte está mal, repruebas aunque hayas rooteado todo.

**Costo aproximado:** USD $210 (voucher de examen) + $14/mes (HTB Student que ya pagas).

---

## Post-CPTS — Hoja de Ruta 2027

Una vez certificado con CPTS + Ingeniería en Ciberseguridad (2027), el perfil es competitivo para posiciones de penetration testing en Chile. El siguiente paso natural es **OSCP+** (OffSec), que abre mercado internacional.

En paralelo, **Proyecto Cóndor** puede evolucionar a una propuesta concreta de Red Team as a Service para el mercado chileno, diferenciada por reporting en español, integración normativa local, y automatización con IA.
