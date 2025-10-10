from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from ..deps import get_db
from ..models import  Estudiante
from Apis.schemas import EstudianteCreate, EstudianteResponse

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("", response_model=List[EstudianteResponse], summary="Listar estudiantes")
async def listar_estudiantes(
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    result = await db.execute(select(Estudiante))
    return result.scalars().all()

@router.post("", response_model=EstudianteResponse, summary="Crear estudiante")
async def crear_estudiante(
    estudiante: EstudianteCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
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

@router.put("/{estudiante_id}", response_model=EstudianteResponse, summary="Actualizar estudiante")
async def actualizar_estudiante(
    estudiante_id: str,
    estudiante: EstudianteCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    q = await db.execute(select(Estudiante).where(Estudiante.id == estudiante_id))
    estudiante_db = q.scalars().first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    estudiante_db.nombre = estudiante.nombre
    estudiante_db.apellido = estudiante.apellido
    estudiante_db.email = estudiante.email
    estudiante_db.actualizado_por = username

    await db.commit()
    await db.refresh(estudiante_db)
    return estudiante_db

@router.delete("/{estudiante_id}", summary="Eliminar estudiante")
async def eliminar_estudiante(
    estudiante_id: str,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(verify_token),
):
    q = await db.execute(select(Estudiante).where(Estudiante.id == estudiante_id))
    estudiante_db = q.scalars().first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    await db.delete(estudiante_db)
    await db.commit()
    return {"detail": "Estudiante eliminado correctamente"}
