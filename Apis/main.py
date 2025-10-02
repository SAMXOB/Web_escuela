from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from Apis.auth import create_access_token, verify_token
from Apis.database import SessionLocal
from Apis.models_sqlalchemy import Usuario, Estudiante, Profesor, Materia, Curso, Inscripcion
from Apis.schemas import (
    UsuarioCreate, UsuarioResponse,
    EstudianteCreate, EstudianteResponse,
    ProfesorCreate, ProfesorResponse,
    MateriaCreate, MateriaResponse,
    CursoCreate, CursoResponse,
    InscripcionCreate, InscripcionResponse
)

app = FastAPI(title="API Escuela - Proyecto Final")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

# ------------------ LOGIN ------------------ #
@app.post("/login", summary="Autenticación de usuario")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Autentica al usuario y devuelve un token JWT.
    """
    query = await db.execute(select(Usuario).where(Usuario.username == form_data.username))
    user = query.scalars().first()
    if user and user.password == form_data.password:
        token = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Credenciales incorrectas")

# ------------------ CRUD USUARIOS ------------------ #
@app.post("/usuarios", response_model=UsuarioResponse, summary="Crear usuario")
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    nuevo = Usuario(username=usuario.username, email=usuario.email, password=usuario.password,
                    creado_por="system", actualizado_por="system")
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

# ------------------ CRUD ESTUDIANTES ------------------ #
@app.post("/estudiantes", response_model=EstudianteResponse, summary="Crear estudiante")
async def crear_estudiante(estudiante: EstudianteCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Crea un nuevo estudiante en la base de datos.
    """
    nuevo = Estudiante(nombre=estudiante.nombre, apellido=estudiante.apellido, email=estudiante.email,
                       creado_por=username, actualizado_por=username)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

@app.get("/estudiantes", response_model=List[EstudianteResponse], summary="Listar estudiantes")
async def listar_estudiantes(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Devuelve la lista completa de estudiantes.
    """
    result = await db.execute(select(Estudiante))
    return result.scalars().all()

# ------------------ CRUD PROFESORES ------------------ #
@app.post("/profesores", response_model=ProfesorResponse, summary="Crear profesor")
async def crear_profesor(profesor: ProfesorCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Crea un nuevo profesor en la base de datos.
    """
    nuevo = Profesor(nombre=profesor.nombre, apellido=profesor.apellido, email=profesor.email,
                     creado_por=username, actualizado_por=username)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

@app.get("/profesores", response_model=List[ProfesorResponse], summary="Listar profesores")
async def listar_profesores(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Devuelve la lista completa de profesores.
    """
    result = await db.execute(select(Profesor))
    return result.scalars().all()

# ------------------ CRUD MATERIAS ------------------ #
@app.post("/materias", response_model=MateriaResponse, summary="Crear materia")
async def crear_materia(materia: MateriaCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Crea una nueva materia en la base de datos.
    """
    nueva = Materia(nombre=materia.nombre, creditos=materia.creditos, profesor_id=materia.profesor_id,
                    creado_por=username, actualizado_por=username)
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

@app.get("/materias", response_model=List[MateriaResponse], summary="Listar materias")
async def listar_materias(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Devuelve la lista completa de materias.
    """
    result = await db.execute(select(Materia))
    return result.scalars().all()

# ------------------ CRUD CURSOS ------------------ #
@app.post("/cursos", response_model=CursoResponse, summary="Crear curso")
async def crear_curso(curso: CursoCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Crea un nuevo curso en la base de datos.
    """
    nuevo = Curso(nombre=curso.nombre, materia_id=curso.materia_id,
                  creado_por=username, actualizado_por=username)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

@app.get("/cursos", response_model=List[CursoResponse], summary="Listar cursos")
async def listar_cursos(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Devuelve la lista completa de cursos.
    """
    result = await db.execute(select(Curso))
    return result.scalars().all()

# ------------------ CRUD INSCRIPCIONES ------------------ #
@app.post("/inscripciones", response_model=InscripcionResponse, summary="Crear inscripción")
async def crear_inscripcion(inscripcion: InscripcionCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Crea una nueva inscripción en la base de datos.
    """
    nueva = Inscripcion(estudiante_id=inscripcion.estudiante_id, curso_id=inscripcion.curso_id,
                         creado_por=username, actualizado_por=username)
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

@app.get("/inscripciones", response_model=List[InscripcionResponse], summary="Listar inscripciones")
async def listar_inscripciones(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    """
    Devuelve la lista completa de inscripciones.
    """
    result = await db.execute(select(Inscripcion))
    return result.scalars().all()