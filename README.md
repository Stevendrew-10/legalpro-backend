# LegalPro - Backend (Gestión de Casos) - SGLPWEB

Backend mínimo funcional para el caso de estudio **LegalPro** (módulo de Gestión de Casos):
- Registro de clientes y casos con **número de caso único**
- Seguimiento de **plazos/calendario** por caso (audiencias, vencimientos, etc.)
- **Asignación de tareas** por caso (prioridad, fecha límite, estado)
- Evidencias por tarea (metadatos / URL o nombre de archivo)
- Portal de cliente **solo lectura** (visualiza casos y avances, no modifica)

> Nota del examen: se implementa únicamente Back-End (API + BD). No incluye Front-End.

## Requisitos
- Python 3.10+ (recomendado 3.11)
- (Opcional) Visual Studio Code

## Instalación y ejecución

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Windows (PowerShell)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Probar en Swagger
- Swagger UI: http://127.0.0.1:8000/docs

## Base de datos
Por defecto usa SQLite local (archivo `legalpro.db`).

Incluye script SQL de referencia:
- `sql/schema.sql`
