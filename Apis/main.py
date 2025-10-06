from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from Apis.auth import create_access_token, verify_token
from Apis.database import SessionLocal
from Apis.models_sqlalchemy import (
    Usuario,
    Estudiante,
    Profesor,
    Materia,
    Curso,
    Inscripcion,
)
from Apis.schemas import (
    UsuarioCreate,
    UsuarioResponse,
    EstudianteCreate,
    EstudianteResponse,
    ProfesorCreate,
    ProfesorResponse,
    MateriaCreate,
    MateriaResponse,
    CursoCreate,
    CursoResponse,
    InscripcionCreate,
    InscripcionResponse,
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
    """
    Proporciona una sesión de base de datos asíncrona.

    Yields:
        AsyncSession: Sesión de base de datos para realizar operaciones.
    """
    async with SessionLocal() as session:
        yield session


# ------------------ LOGIN ------------------ #
@app.post("/login", summary="Autenticación de usuario")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Autentica al usuario y devuelve un token JWT.

    Args:
        form_data (OAuth2PasswordRequestForm): Datos del formulario de autenticación.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.

    Returns:
        dict: Un diccionario con el token de acceso y su tipo.

    Raises:
        HTTPException: Si las credenciales son incorrectas.
    """
    query = await db.execute(
        select(Usuario).where(Usuario.username == form_data.username)
    )
    user = query.scalars().first()
    if user and user.password == form_data.password:
        token = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Credenciales incorrectas")


# ------------------ CRUD USUARIOS ------------------ #
@app.get(
    "/usuarios",
    response_model=List[UsuarioResponse],
    summary="Listar usuarios",
)
async def listar_usuarios(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de los usuario.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[UsuarioResponsee]: Lista de usuarios.
    """
    result = await db.execute(select(Usuario))
    return result.scalars().all()


@app.post("/usuarios", response_model=UsuarioResponse, summary="Crear usuario")
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        usuario (UsuarioCreate): Datos del usuario a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.

    Returns:
        UsuarioResponse: El usuario creado.
    """
    nuevo = Usuario(
        username=usuario.username,
        email=usuario.email,
        password=usuario.password,
        creado_por="system",
        actualizado_por="system",
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@app.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
)
async def actualizar_usuario(
    usuario_id: str,
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza un usuario existente en la base de datos.

    Args:
        usuario_id (str): ID del usuario a actualizar.
        usuario (UsuarioCreate): Datos actualizados del usuario.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        UsuarioResponse: El usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    query = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = query.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_db.username = usuario.username
    usuario_db.email = usuario.email
    usuario_db.password = usuario.password
    usuario_db.actualizado_por = username

    await db.commit()
    await db.refresh(usuario_db)
    return usuario_db


@app.delete("/usuarios/{usuario_id}", summary="Eliminar usuario")
async def eliminar_usuario(
    usuario_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina un usuario de la base de datos.

    Args:
        usuario_id (str): ID del usuario a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    query = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = query.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await db.delete(usuario_db)
    await db.commit()
    return {"detail": "Usuario eliminado correctamente"}


# ------------------ CRUD ESTUDIANTES ------------------ #
@app.get(
    "/estudiantes",
    response_model=List[EstudianteResponse],
    summary="Listar estudiantes",
)
async def listar_estudiantes(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de estudiantes.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[EstudianteResponse]: Lista de estudiantes.
    """
    result = await db.execute(select(Estudiante))
    return result.scalars().all()


@app.post("/estudiantes", response_model=EstudianteResponse, summary="Crear estudiante")
async def crear_estudiante(
    estudiante: EstudianteCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Crea un nuevo estudiante en la base de datos.

    Args:
        estudiante (EstudianteCreate): Datos del estudiante a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        EstudianteResponse: El estudiante creado.
    """
    nuevo = Estudiante(
        nombre=estudiante.nombre,
        apellido=estudiante.apellido,
        email=estudiante.email,
        creado_por=username,
        actualizado_por=username,
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@app.put(
    "/estudiantes/{estudiante_id}",
    response_model=EstudianteResponse,
    summary="Actualizar estudiante",
)
async def actualizar_estudiante(
    estudiante_id: str,
    estudiante: EstudianteCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza un estudiante existente en la base de datos.

    Args:
        estudiante_id (str): ID del estudiante a actualizar.
        estudiante (EstudianteCreate): Datos actualizados del estudiante.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        EstudianteResponse: El estudiante actualizado.

    Raises:
        HTTPException: Si el estudiante no existe.
    """
    query = await db.execute(select(Estudiante).where(Estudiante.id == estudiante_id))
    estudiante_db = query.scalars().first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    estudiante_db.nombre = estudiante.nombre
    estudiante_db.apellido = estudiante.apellido
    estudiante_db.email = estudiante.email
    estudiante_db.actualizado_por = username

    await db.commit()
    await db.refresh(estudiante_db)
    return estudiante_db


@app.delete("/estudiantes/{estudiante_id}", summary="Eliminar estudiante")
async def eliminar_estudiante(
    estudiante_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina un estudiante de la base de datos.

    Args:
        estudiante_id (str): ID del estudiante a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el estudiante no existe.
    """
    query = await db.execute(select(Estudiante).where(Estudiante.id == estudiante_id))
    estudiante_db = query.scalars().first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    await db.delete(estudiante_db)
    await db.commit()
    return {"detail": "Estudiante eliminado correctamente"}


# ------------------ CRUD PROFESORES ------------------ #
@app.get(
    "/profesores", response_model=List[ProfesorResponse], summary="Listar profesores"
)
async def listar_profesores(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de profesores.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[ProfesorResponse]: Lista de profesores.
    """
    result = await db.execute(select(Profesor))
    return result.scalars().all()


@app.post("/profesores", response_model=ProfesorResponse, summary="Crear profesor")
async def crear_profesor(
    profesor: ProfesorCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Crea un nuevo profesor en la base de datos.

    Args:
        profesor (ProfesorCreate): Datos del profesor a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        ProfesorResponse: El profesor creado.
    """
    nuevo = Profesor(
        nombre=profesor.nombre,
        apellido=profesor.apellido,
        email=profesor.email,
        creado_por=username,
        actualizado_por=username,
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@app.put(
    "/profesores/{profesor_id}",
    response_model=ProfesorResponse,
    summary="Actualizar profesor",
)
async def actualizar_profesor(
    profesor_id: str,
    profesor: ProfesorCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza un profesor existente en la base de datos.

    Args:
        profesor_id (str): ID del profesor a actualizar.
        profesor (ProfesorCreate): Datos actualizados del profesor.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        ProfesorResponse: El profesor actualizado.

    Raises:
        HTTPException: Si el profesor no existe.
    """
    query = await db.execute(select(Profesor).where(Profesor.id == profesor_id))
    profesor_db = query.scalars().first()
    if not profesor_db:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    profesor_db.nombre = profesor.nombre
    profesor_db.apellido = profesor.apellido
    profesor_db.email = profesor.email
    profesor_db.actualizado_por = username

    await db.commit()
    await db.refresh(profesor_db)
    return profesor_db


@app.delete("/profesores/{profesor_id}", summary="Eliminar profesor")
async def eliminar_profesor(
    profesor_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina un profesor de la base de datos.

    Args:
        profesor_id (str): ID del profesor a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el profesor no existe.
    """
    query = await db.execute(select(Profesor).where(Profesor.id == profesor_id))
    profesor_db = query.scalars().first()
    if not profesor_db:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    await db.delete(profesor_db)
    await db.commit()
    return {"detail": "Profesor eliminado correctamente"}


# ------------------ CRUD MATERIAS ------------------ #


@app.get("/materias", response_model=List[MateriaResponse], summary="Listar materias")
async def listar_materias(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de materias.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[MateriaResponse]: Lista de materias.
    """
    result = await db.execute(select(Materia))
    return result.scalars().all()


@app.post("/materias", response_model=MateriaResponse, summary="Crear materia")
async def crear_materia(
    materia: MateriaCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Crea una nueva materia en la base de datos.

    Args:
        materia (MateriaCreate): Datos de la materia a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        MateriaResponse: La materia creada.
    """
    nueva = Materia(
        nombre=materia.nombre,
        creditos=materia.creditos,
        profesor_id=materia.profesor_id,
        creado_por=username,
        actualizado_por=username,
    )
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva


@app.put(
    "/materias/{materia_id}",
    response_model=MateriaResponse,
    summary="Actualizar materia",
)
async def actualizar_materia(
    materia_id: str,
    materia: MateriaCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza una materia existente en la base de datos.

    Args:
        materia_id (str): ID de la materia a actualizar.
        materia (MateriaCreate): Datos actualizados de la materia.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        MateriaResponse: La materia actualizada.

    Raises:
        HTTPException: Si la materia no existe.
    """
    query = await db.execute(select(Materia).where(Materia.id == materia_id))
    materia_db = query.scalars().first()
    if not materia_db:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    materia_db.nombre = materia.nombre
    materia_db.creditos = materia.creditos
    materia_db.profesor_id = materia.profesor_id
    materia_db.actualizado_por = username

    await db.commit()
    await db.refresh(materia_db)
    return materia_db


@app.delete("/materias/{materia_id}", summary="Eliminar materia")
async def eliminar_materia(
    materia_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina una materia de la base de datos.

    Args:
        materia_id (str): ID de la materia a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si la materia no existe.
    """
    query = await db.execute(select(Materia).where(Materia.id == materia_id))
    materia_db = query.scalars().first()
    if not materia_db:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    await db.delete(materia_db)
    await db.commit()
    return {"detail": "Materia eliminada correctamente"}


# ------------------ CRUD CURSOS ------------------ #
@app.get("/cursos", response_model=List[CursoResponse], summary="Listar cursos")
async def listar_cursos(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de cursos.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[CursoResponse]: Lista de cursos.
    """
    result = await db.execute(select(Curso))
    return result.scalars().all()


@app.post("/cursos", response_model=CursoResponse, summary="Crear curso")
async def crear_curso(
    curso: CursoCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Crea un nuevo curso en la base de datos.

    Args:
        curso (CursoCreate): Datos del curso a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        CursoResponse: El curso creado.
    """
    nuevo = Curso(
        nombre=curso.nombre,
        materia_id=curso.materia_id,
        creado_por=username,
        actualizado_por=username,
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@app.put("/cursos/{curso_id}", response_model=CursoResponse, summary="Actualizar curso")
async def actualizar_curso(
    curso_id: str,
    curso: CursoCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza un curso existente en la base de datos.

    Args:
        curso_id (str): ID del curso a actualizar.
        curso (CursoCreate): Datos actualizados del curso.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        CursoResponse: El curso actualizado.

    Raises:
        HTTPException: Si el curso no existe.
    """
    query = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso_db = query.scalars().first()
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    curso_db.nombre = curso.nombre
    curso_db.materia_id = curso.materia_id
    curso_db.actualizado_por = username

    await db.commit()
    await db.refresh(curso_db)
    return curso_db


@app.delete("/cursos/{curso_id}", summary="Eliminar curso")
async def eliminar_curso(
    curso_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina un curso de la base de datos.

    Args:
        curso_id (str): ID del curso a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el curso no existe.
    """
    query = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso_db = query.scalars().first()
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    await db.delete(curso_db)
    await db.commit()
    return {"detail": "Curso eliminado correctamente"}


# ------------------ CRUD INSCRIPCIONES ------------------ #


@app.get(
    "/inscripciones",
    response_model=List[InscripcionResponse],
    summary="Listar inscripciones",
)
async def listar_inscripciones(
    db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    """
    Devuelve la lista completa de inscripciones.

    Args:
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        List[InscripcionResponse]: Lista de inscripciones.
    """
    result = await db.execute(select(Inscripcion))
    return result.scalars().all()


@app.post(
    "/inscripciones", response_model=InscripcionResponse, summary="Crear inscripción"
)
async def crear_inscripcion(
    inscripcion: InscripcionCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Crea una nueva inscripción en la base de datos.

    Args:
        inscripcion (InscripcionCreate): Datos de la inscripción a crear.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        InscripcionResponse: La inscripción creada.
    """
    nueva = Inscripcion(
        estudiante_id=inscripcion.estudiante_id,
        curso_id=inscripcion.curso_id,
        creado_por=username,
        actualizado_por=username,
    )
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva


@app.put(
    "/inscripciones/{inscripcion_id}",
    response_model=InscripcionResponse,
    summary="Actualizar inscripción",
)
async def actualizar_inscripcion(
    inscripcion_id: str,
    inscripcion: InscripcionCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Actualiza una inscripción existente en la base de datos.

    Args:
        inscripcion_id (str): ID de la inscripción a actualizar.
        inscripcion (InscripcionCreate): Datos actualizados de la inscripción.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        InscripcionResponse: La inscripción actualizada.

    Raises:
        HTTPException: Si la inscripción no existe.
    """
    query = await db.execute(
        select(Inscripcion).where(Inscripcion.id == inscripcion_id)
    )
    inscripcion_db = query.scalars().first()
    if not inscripcion_db:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    inscripcion_db.estudiante_id = inscripcion.estudiante_id
    inscripcion_db.curso_id = inscripcion.curso_id
    inscripcion_db.actualizado_por = username

    await db.commit()
    await db.refresh(inscripcion_db)
    return inscripcion_db


@app.delete("/inscripciones/{inscripcion_id}", summary="Eliminar inscripción")
async def eliminar_inscripcion(
    inscripcion_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    """
    Elimina una inscripción de la base de datos.

    Args:
        inscripcion_id (str): ID de la inscripción a eliminar.
        db (AsyncSession): Sesión de base de datos proporcionada por la dependencia.
        username (str): Nombre de usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si la inscripción no existe.
    """
    query = await db.execute(
        select(Inscripcion).where(Inscripcion.id == inscripcion_id)
    )
    inscripcion_db = query.scalars().first()
    if not inscripcion_db:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    await db.delete(inscripcion_db)
    await db.commit()
    return {"detail": "Inscripción eliminada correctamente"}
