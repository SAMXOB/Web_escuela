# Web Escuela — API

API REST para la gestión de estudiantes, profesores y materias. Fue desarrollada como parte de la asignatura Aplicaciones y Servicios Web.

## Funcionalidades

- Operaciones CRUD para estudiantes, profesores y materias.
- Validación de datos mediante modelos Pydantic.
- Filtrado por materia.
- Manejo de errores comunes, como identificadores duplicados o recursos inexistentes.

## Tecnologías

- Python 3.9 o superior
- FastAPI
- Uvicorn
- Pydantic

## Estructura

```text
Web_escuela/
├── main.py     # Aplicación y endpoints
├── models.py   # Modelos y validaciones
├── data.py     # Almacenamiento temporal en memoria
└── README.md
```

## Proyecto relacionado

- Frontend: [WebEscuelaFrontEnd](https://github.com/SAMXOB/WebEscuelaFrontEnd)
