# 🚀 Examen Práctico de DevOps - Aplicación Flask & PostgreSQL

Este repositorio contiene la solución completa para el **Examen Práctico de DevOps**. Consiste en una aplicación web desarrollada en **Flask** que interactúa con un motor de base de datos **PostgreSQL 17** y un administrador web **pgAdmin 4**. Todo el sistema está completamente contenedorizado, interconectado mediante redes aisladas de Docker, y automatizado con un pipeline de **GitHub Actions** hacia **GitHub Container Registry (GHCR)**.

---

## 🛠️ Stack Tecnológico
* **Backend:** Python 3.12-slim & Flask 3.1
* **Base de Datos:** PostgreSQL 17 (Alpine Linux)
* **Administración DB:** pgAdmin 4
* **Orquestación:** Docker Compose V2
* **CI/CD & Registro:** GitHub Actions & GHCR (GitHub Container Registry)

---

## 📋 Variables de Entorno e Inyección de Datos (Rúbrica: 1.5 Puntos)

Para cumplir con los requerimientos de seguridad y desacoplamiento, la aplicación Flask no tiene credenciales fijas (*hardcoded*). En su lugar, lee las configuraciones dinámicamente desde el entorno usando el módulo `os` de Python:

| Variable en Flask | Variable Inyectada (Compose) | Propósito | Valor por Defecto |
| :--- | :--- | :--- | :--- |
| `APP_NAME` | `- APP_NAME=...` | Define el nombre dinámico del sitio web | Examen Practico DevOps |
| `VERSION` | `- APP_VERSION=...` | Controla el versionamiento visible en el frontend | `1.0.0` / `2.0.0` |
| `DB_HOST` | `- DB_HOST=db` | Apunta al nombre del servicio base en la red | `db` |
| `DB_NAME` | `- DB_NAME=empresa` | Nombre de la base de datos a conectar | `empresa` |
| `DB_USER` | `- DB_USER=admin` | Usuario administrador de PostgreSQL | `admin` |
| `DB_PASSWORD` | `- DB_PASSWORD=...` | Contraseña de acceso a la base de datos | `admin123` |

---

## ⚙️ Arquitectura de Red y Persistencia (Rúbrica: 2.5 Puntos)

### 1. Persistencia con Volúmenes
Se configuró un volumen nombrado llamado `postgres_data` asignado a la ruta interna `/var/lib/postgresql/data` del contenedor de la base de datos. Esto garantiza que, aunque los contenedores se detengan o destruyan, los productos registrados no se pierdan.

### 2. Red Aislada (`red-examen`)
Los 3 servicios coexisten en una red con driver `bridge` llamada `red-examen`. Esto permite que Flask se comunique con PostgreSQL usando el hostname `db` de forma segura, aislando el tráfico de bases de datos del exterior.

---

## 🚀 Instrucciones de Despliegue Local

### Paso 1: Clonar y Construir el Entorno
Ejecute el siguiente comando en la terminal (PowerShell / Bash) dentro de la raíz del proyecto para compilar la imagen local de Flask y descargar los servicios oficiales:
```bash
docker compose up -d --build