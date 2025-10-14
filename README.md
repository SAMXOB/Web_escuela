# API Escuela

## AUTORES
- **Samuel Orozco Bedoya**  
- **Héctor Daniel Sánchez Muñoz** 
---

## TÍTULO DEL PROYECTO
API RESTful para la gestión de Estudiantes, Profesores, Materias, Cursos, Inscripciones, Usuarios

---

## DESCRIPCIÓN
Este proyecto implementa una API RESTful orientada a la gestión académica de una escuela. Permite administrar Estudiantes, Profesores, Materias, Cursos, Inscripciones, Usuarios, ofreciendo operaciones CRUD completas, autenticación mediante JWT y conexión a base de datos relacional.  
El objetivo es proporcionar un sistema escalable y seguro que facilite la administración de datos académicos y garantice la integridad de la información.

---

## ARQUITECTURA
Se utiliza una arquitectura basada en capas con **FastAPI**, organizada para mantener el código limpio y escalable. Las principales capas son:

- **Apis/**: Contiene los endpoints organizados por entidad.
- **Models/**: Define las clases que representan las tablas en la base de datos usando **SQLAlchemy**.
- **Schemas/**: Clases Pydantic para validación y serialización de datos.
- **Database/**: Configuración de la conexión a la base de datos y gestión de sesiones.
- **Auth/**: Implementación de autenticación JWT.
- **main.py**: Punto de entrada de la aplicación.

---

## REQUISITOS DE INSTALACIÓN
- **Python 3.10+**
- Dependencias principales:
  - fastapi
  - uvicorn
  - SQLAlchemy
  - psycopg2 (o asyncpg si usas asincronía)
  - python-jose (para JWT)
  - passlib (para hashing de contraseñas)
  - pydantic

Instalación:

pip install -r requirements.txt

CONFIGURACIÓN
Crear un archivo .env con las variables necesarias:
DATABASE_URL=postgresql+psycopg2://usuario:password@host:puerto/dbname
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


INSTRUCCIONES DE EJECUCIÓN
Levantar el servidor:
uvicorn main:app --reload

Acceder a la documentación:

Swagger: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc


DESCRIPCIÓN DE ENDPOINTS
🔐 Autenticación

POST /auth/login → Genera token JWT para autenticación.
POST /auth/register → Registra un nuevo usuario.

👩‍🎓 Estudiantes

GET /estudiantes → Lista todos los estudiantes (filtrado opcional por materia).
GET /estudiantes/{id} → Obtiene un estudiante por ID.
POST /estudiantes → Crea un nuevo estudiante.
PUT /estudiantes/{id} → Actualiza un estudiante.
DELETE /estudiantes/{id} → Elimina un estudiante.

👨‍🏫 Profesores

CRUD completo similar a estudiantes.

📚 Materias

CRUD completo similar a estudiantes.


DOCUMENTACIÓN EXTRA

Swagger UI
ReDoc


NOTAS
Este proyecto sigue buenas prácticas de desarrollo, incluyendo:

Manejo de errores.
Validación de datos.
Autenticación segura.
Arquitectura modular.
