# Repaso — Escaneo de Servicios (HTB Academy · Getting Started §7)

> Nota de repaso auto-generada tras autoevaluación (25-sep-2026).
> Contiene **solo lo que fallé o dejé flojo**, no lo que ya domino.

## 1. `-sC` — corrección de concepto

`-sC` **no** "prueba si el objetivo es vulnerable a un script". Ejecuta los NSE de la
categoría **`default`**, cuyo trabajo es **enumerar información extra**:

- `http-title`, `http-server-header` en webs
- `ftp-anon` (login anónimo permitido)
- `smb-os-discovery`, `smb2-security-mode`
- banners de servicio

Algunos scripts default rozan vulnerabilidades conocidas, pero la categoría es de
*información*, no de explotación.

| Flag | Qué hace |
|------|----------|
| `-sV` | Escaneo de **versión** del servicio en cada puerto abierto |
| `-sC` | Corre los scripts NSE **default** (info extra) |
| `-p-` | Escanea los **65535** puertos TCP |

## 2. SMB — enumeración de shares

```bash
smbclient -N -L \\\\10.129.42.253            # listar shares sin credenciales
smbclient -U bob \\\\10.129.42.253\\users     # conectar a un share como user
```

- `-L` → lista los recursos compartidos (shares)
- `-N` → suprime el prompt de contraseña (null session)
- `-U <user>` → fuerza el usuario para autenticarse

Dentro del prompt `smb: \>` funcionan `ls`, `cd`, `get archivo.txt`.

Script Nmap útil para versión de SO vía SMB:
```bash
nmap --script smb-os-discovery.nse -p445 <IP>
```

## 3. SNMP — por qué v1/v2c es un regalo

- En **v1 y v2c** la *community string* viaja en **texto plano, sin cifrado ni
  autenticación**. El cifrado/auth recién aparece en **v3**.
- Si adivinas o snifeas la string, lees: procesos en ejecución (a veces con
  **credenciales en la línea de comandos**), tablas de ruteo, versiones de software.
- Primeras strings a probar (defaults de fábrica): **`public`** y **`private`**.

```bash
snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0   # consulta puntual
snmpwalk -v 2c -c public 10.129.42.253                     # walk completo
onesixtyone -c dict.txt 10.129.42.253                      # fuerza bruta de strings
```

## 4. ¿Qué vería un Threat Hunter? (perspectiva Blue Team)

Un escaneo `nmap -p- -sV -sC` no se detecta por "volumen de tráfico", sino por la
**firma de escaneo**:

- **1 IP origen → cientos/miles de puertos distintos** del mismo destino en segundos
  (patrón vertical: un host, muchos puertos).
- Ráfaga de paquetes **SYN**; muchos **RST** de vuelta desde puertos cerrados.
- Con `-sV`/`-sC`: **payloads de sondeo a nivel de aplicación** (banners, tráfico de
  scripts NSE), no solo handshakes vacíos.
- El IDS (Suricata/Snort) lo etiqueta como `port scan` / `scan detected`.

> Regla clave: lo que delata es el patrón **1 origen → N puertos**, no la cantidad de
> tráfico.

## Detalle menor a recordar

- `ftp -p <IP>` fuerza **modo pasivo** (el cliente abre la conexión de datos), útil
  cuando hay NAT o firewall de por medio.
