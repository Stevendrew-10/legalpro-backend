# LegalPro - Backend (Gestión de casos) - SGLPWEB - Steven Freire

Backend mínimo funcional para el caso de estudio LegalPro
(módulo de Gestión de Casos del sistema SGLPWEB).

> Nota del examen:
> Este proyecto implementa únicamente el Back-End (API + Base de Datos),
> conforme a lo solicitado en el enunciado.  
> No incluye Front-End.

## Funcionalidades principales
- Registro de clientes.
- Registro de casos legales con número de caso único.
- Seguimiento de plazos y calendario por caso (audiencias, vencimientos, etc.).
- Gestión de tareas por caso (prioridad, fecha límite y estado).
- Registro de evidencias por tarea (metadatos / URL / nombre de archivo).
- Portal de cliente solo lectura (visualización de casos y avances).

---

## Arquitectura
La solución utiliza una arquitectura N-Capas, separando:
- **Presentación:** API REST (FastAPI).
- **Lógica de negocio:** validaciones y reglas del sistema.
- **Acceso a datos:** SQLAlchemy ORM.
- **Persistencia:** Base de datos relacional.

Esta arquitectura facilita el mantenimiento, la escalabilidad y la separación de responsabilidades.

---

## Requisitos
- Python 3.10+ (recomendado 3.11)
- (Opcional) Visual Studio Code

---

## Instalación y ejecución

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
