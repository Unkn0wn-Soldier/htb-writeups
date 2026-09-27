---
tags:
  - tecnica
  - categoria/enumeracion
  - os/agnostico
  - nivel/facil
fecha_aprendida: 2026-09-25
fuente: HTB Academy - Getting Started §7
---
# ⚔️ SNMP Enumeration

> [!abstract] Resumen
> SNMP v1/v2c transmite la *community string* (su "contraseña") en texto plano y sin autenticación real. Si se adivina o se sniffea, se puede leer configuración, procesos y a veces credenciales del objetivo.

---

## ¿Qué es y por qué funciona?

SNMP (Simple Network Management Protocol) se usa para monitorear/gestionar dispositivos de red. En v1 y v2c, la única "autenticación" es la *community string*, que viaja sin cifrar. Recién en v3 aparece cifrado y auth real. Si la string es una por defecto (`public` de solo lectura, `private` de lectura/escritura) o se logra sniffear/fuerza bruta, se obtiene acceso de lectura (o escritura) a la MIB del dispositivo: procesos en ejecución (a veces con credenciales en la línea de comandos), tablas de ruteo, versiones de software instalado.

---

## Condiciones necesarias para que aplique

> [!warning] Requisitos
> - Puerto UDP 161 abierto (SNMP)
> - Servicio corriendo v1 o v2c (v3 no es vulnerable a este vector)
> - Community string por defecto o débil

---

## Procedimiento

### Detección / Enumeración

```bash
nmap -sU -p161 --open <IP>
```

### Explotación

```bash
# Fuerza bruta de community strings
onesixtyone -c dict.txt <IP>

# Consulta puntual (un OID específico)
snmpwalk -v 2c -c public <IP> 1.3.6.1.2.1.1.5.0

# Walk completo de la MIB
snmpwalk -v 2c -c public <IP>
```

> [!tip] Variaciones comunes
> - Probar `public` y `private` primero (defaults de fábrica) antes de fuerza bruta con diccionario.

---

## Herramientas asociadas

| Herramienta | Función | Comando base |
| ----------- | ------- | ------------ |
| `snmpwalk` | Recorre la MIB completa o un OID puntual | `snmpwalk -v 2c -c <string> <IP>` |
| `onesixtyone` | Fuerza bruta de community strings | `onesixtyone -c dict.txt <IP>` |

---

## Contramedidas (defensa)

> [!info] ¿Cómo se previene?
> Migrar a SNMPv3 (auth + cifrado), cambiar community strings por defecto, restringir el acceso SNMP por ACL/firewall a IPs de gestión.

---

## Dónde la usé

- Pendiente — repaso teórico HTB Academy, sin aplicación en máquina aún.

---

## Referencias

- [MITRE ATT&CK - T1046 (Network Service Discovery)](https://attack.mitre.org/techniques/T1046/)
