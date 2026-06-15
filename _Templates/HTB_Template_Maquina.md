---
tags:
  - htb
  - starting-point   # o retired
  - tier-0           # tier-0 / tier-1 / tier-2 / phase-1 / etc.
  - easy             # easy / medium / hard
  - linux            # linux / windows / freebsd
  - TECNICA          # etiqueta de técnica principal (ftp, smb, sqli, etc.)
  - en-progreso      # en-progreso / Terminada
ip: 10.10.10.XXX
os: Linux
difficulty: Easy
status: en-progreso
tiempo: 0h 0m
fecha_inicio: <% tp.date.now("YYYY-MM-DD") %>
fecha_completada: —
puntos: 0
mitre_tactics: []
mitre_techniques: []
---

# 🖥️ [Máquina] — [OS] — [Dificultad] ([Fase])

> [!info] Resumen
> **IP:** `10.10.10.XXX` | **OS:** Linux/Windows | **Tier/Fase:** X | **Tiempo:** Xh Xm
> Una línea: qué expone la máquina y cómo se compromete.

---

## 1. Reconocimiento

```bash
nmap -sCV -p- --min-rate 5000 10.10.10.XXX -oN nmap.txt
```

| Puerto | Servicio | Versión | Hallazgo clave |
|--------|----------|---------|----------------|
| XX/TCP | nombre   | X.X     | observación relevante |

**→ Vector:** qué servicio/puerto es el camino y por qué.

---

## 2. Explotación

> Vector principal: [nombre de la vulnerabilidad/misconfiguration]

```bash
# Comandos exactos que funcionaron
# Con flags y parámetros reales
```

> [!success] Flag / Acceso obtenido
> `hash_o_descripción`

---

## 3. Escalación de Privilegios *(si aplica)*

```bash
# Enumeración clave
sudo -l / find / -perm -4000 / cat /etc/crontab

# Exploit de privesc
```

> [!success] Root/System flag
> `hash`

---

## 4. MITRE ATT&CK

| Táctica | Técnica | ID | Uso en esta máquina |
|---------|---------|----|---------------------|
| Initial Access | Nombre | TXXXX | descripción breve |

---

## 5. Detección & Remediación

**Blue Team detecta:** (2-3 bullets máximo)
- Log / evento detectable

**Remediación:** (2-3 bullets máximo)
- Fix concreto

---

## 6. Lecciones

- Punto 1: técnica nueva o confirmada
- Punto 2: error cometido y fix
- Punto 3: conexión con concepto mayor (opcional)

**Bloqueado:**
| Fase | Causa | Fix |
|------|-------|-----|
| — | — | — |

---

## 7. Conexiones

- Similar: `[[HTB/Maquina/Maquina]]`
- Siguiente nivel: `[[HTB/Maquina/Maquina]]`
- Técnica: `[[Técnicas/Nombre]]`

**Referencias:** [HackTricks](url) · [CVE](url) · [IppSec](url)
