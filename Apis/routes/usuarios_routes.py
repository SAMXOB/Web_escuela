from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from ..deps import get_db
from ..models import Usuario
from Apis.schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("", response_model=List[UsuarioResponse], summary="Listar usuarios")
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Usuario))
    return result.scalars().all()

@router.post("", response_model=UsuarioResponse, summary="Crear usuario")
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
):
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

@router.put("/{usuario_id}", response_model=UsuarioResponse, summary="Actualizar usuario")
async def actualizar_usuario(
    usuario_id: str,
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    q = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = q.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_db.username = usuario.username
    usuario_db.email = usuario.email
    usuario_db.password = usuario.password
    usuario_db.actualizado_por = username

    await db.commit()
    await db.refresh(usuario_db)
    return usuario_db

@router.delete("/{usuario_id}", summary="Eliminar usuario")
async def eliminar_usuario(
    usuario_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    q = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario_db = q.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await db.delete(usuario_db)
    await db.commit()
    return {"detail": "Usuario eliminado correctamente"}
