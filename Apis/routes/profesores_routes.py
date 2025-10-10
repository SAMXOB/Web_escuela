from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from Apis.deps import get_db
from ..deps import get_db
from ..models import  Profesor
from Apis.schemas import ProfesorCreate, ProfesorResponse

router = APIRouter(prefix="/profesores", tags=["Profesores"])

@router.get("", response_model=List[ProfesorResponse], summary="Listar profesores")
async def listar_profesores(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    res = await db.execute(select(Profesor))
    return res.scalars().all()

@router.post("", response_model=ProfesorResponse, summary="Crear profesor")
async def crear_profesor(
    profesor: ProfesorCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    nuevo = Profesor(nombre=profesor.nombre, apellido=profesor.apellido, email=profesor.email,
                     creado_por=username, actualizado_por=username)
    db.add(nuevo); await db.commit(); await db.refresh(nuevo); return nuevo

@router.put("/{profesor_id}", response_model=ProfesorResponse, summary="Actualizar profesor")
async def actualizar_profesor(
    profesor_id: str, profesor: ProfesorCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    q = await db.execute(select(Profesor).where(Profesor.id == profesor_id))
    profesor_db = q.scalars().first()
    if not profesor_db: raise HTTPException(status_code=404, detail="Profesor no encontrado")
    profesor_db.nombre = profesor.nombre; profesor_db.apellido = profesor.apellido
    profesor_db.email = profesor.email; profesor_db.actualizado_por = username
    await db.commit(); await db.refresh(profesor_db); return profesor_db

@router.delete("/{profesor_id}", summary="Eliminar profesor")
async def eliminar_profesor(profesor_id: str, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Profesor).where(Profesor.id == profesor_id))
    profesor_db = q.scalars().first()
    if not profesor_db: raise HTTPException(status_code=404, detail="Profesor no encontrado")
    await db.delete(profesor_db); await db.commit(); return {"detail": "Profesor eliminado correctamente"}
