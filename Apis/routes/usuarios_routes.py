from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from Apis.auth import verify_token
from ..deps import get_db
from ..models import Usuario
from Apis.schemas import UsuarioCreate, UsuarioResponse
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# --- Schemas ---
class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# --- Rutas ---
@router.get("", response_model=List[UsuarioResponse], summary="Listar usuarios")
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Usuario))
    return result.scalars().all()

@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario por id")
async def obtener_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
):
    nuevo = Usuario(
        username=usuario.username,
        email=usuario.email,
        password=usuario.password,  # TIP: hashea antes de guardar
        creado_por="system",
        actualizado_por="system",
    )
    db.add(nuevo)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El email ya existe") from e
    await db.refresh(nuevo)
    return nuevo

@router.put("/{usuario_id}", response_model=UsuarioResponse, summary="Actualizar usuario")
async def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = result.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = usuario.model_dump(exclude_unset=True)

    # Si envían password, actualízala (ideal: hasheada)
    if "password" in data and data["password"] is not None:
        usuario_db.password = data.pop("password")

    for k, v in data.items():
        setattr(usuario_db, k, v)

    usuario_db.actualizado_por = username

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El email ya existe") from e

    await db.refresh(usuario_db)
    return usuario_db

@router.delete("/{usuario_id}", summary="Eliminar usuario")
async def eliminar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = result.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # OJO: delete no es async
    db.delete(usuario_db)
    await db.commit()
    return {"detail": "Usuario eliminado correctamente"}
