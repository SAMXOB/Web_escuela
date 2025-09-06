API Escuela - Parcial 1
1. Título del Proyecto

API RESTful para la gestión de Estudiantes, Profesores y Materias

2. Descripción General

Este proyecto implementa una API RESTful básica utilizando FastAPI como parte del Parcial 1 de la materia Aplicaciones y Servicios Web.

La API permite gestionar la información de una escuela mediante operaciones CRUD sobre tres entidades principales:

Estudiantes

Profesores

Materias

Problema que resuelve

Permite registrar y consultar de manera sencilla los datos de los estudiantes, profesores y materias, además de realizar filtrados por materia, validaciones y manejar errores comunes (IDs duplicados, elementos no encontrados, etc.).

3. Arquitectura o Diseño

El proyecto está organizado de la siguiente manera:

Web_escuela/
│
├── main.py     # Punto de entrada, define la aplicación y los endpoints
├── models.py   # Modelos de datos con Pydantic (Estudiante, Profesor, Materia)
├── data.py     # "Base de datos" simulada en memoria (listas con objetos)
└── README.md   # Documentación del proyecto


Explicación breve:

models.py: Define la estructura de las entidades (validaciones y tipos).

data.py: Contiene listas que actúan como almacenamiento temporal.

main.py: Implementa la lógica de negocio y expone los endpoints de la API.

4. Requisitos de Instalación

Python 3.9+ (recomendado 3.10 o superior)

Dependencias principales:

FastAPI

Uvicorn

Instalación de dependencias:

pip install fastapi uvicorn

5. Instrucciones de Ejecución

Clonar el repositorio:

git clone https://github.com/TU_USUARIO/api_universitaria.git


Ejecutar el servidor con Uvicorn:

uvicorn main:app --reload


Acceder a la API en:

Documentación Swagger (interactiva):
👉 http://127.0.0.1:8000/docs

Documentación ReDoc (alternativa):
👉 http://127.0.0.1:8000/redoc

6. Descripción de Endpoints
Estudiantes

GET /estudiantes → Lista todos los estudiantes (soporta query param materia_id).
Ejemplo: /estudiantes?materia_id=1

GET /estudiantes/{id} → Obtiene un estudiante por ID.

POST /estudiantes → Crea un nuevo estudiante (JSON en body).

PUT /estudiantes/{id} → Actualiza un estudiante por ID.

DELETE /estudiantes/{id} → Elimina un estudiante por ID.

Profesores

GET /profesores → Lista todos los profesores.

POST /profesores → Crea un nuevo profesor.

PUT /profesores/{id} → Actualiza un profesor por ID.

DELETE /profesores/{id} → Elimina un profesor por ID.

Materias

GET /materia → Lista todas las materias.

POST /materia → Crea una nueva materia.

PUT /materia/{id} → Actualiza una materia por ID.

DELETE /materia/{id} → Elimina una materia por ID.

7. Autores / Integrantes del Grupo

Samuel Orozco Bedoya – CRUD de Estudiantes + parte de Profesores

Héctor Daniel Sánchez Muñoz – CRUD de Materias + parte de Profesores
