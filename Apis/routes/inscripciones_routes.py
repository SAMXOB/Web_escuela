from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from Apis.deps import get_db
from ..deps import get_db
from ..models import  Inscripcion
from Apis.schemas import InscripcionCreate, InscripcionResponse

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])

@router.get("", response_model=List[InscripcionResponse], summary="Listar inscripciones")
async def listar_inscripciones(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    res = await db.execute(select(Inscripcion)); return res.scalars().all()

@router.post("", response_model=InscripcionResponse, summary="Crear inscripción")
async def crear_inscripcion(
    inscripcion: InscripcionCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    nueva = Inscripcion(estudiante_id=inscripcion.estudiante_id, curso_id=inscripcion.curso_id,
                        creado_por=username, actualizado_por=username)
    db.add(nueva); await db.commit(); await db.refresh(nueva); return nueva

@router.put("/{inscripcion_id}", response_model=InscripcionResponse, summary="Actualizar inscripción")
async def actualizar_inscripcion(
    inscripcion_id: str, inscripcion: InscripcionCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)
):
    q = await db.execute(select(Inscripcion).where(Inscripcion.id == inscripcion_id))
    inscripcion_db = q.scalars().first()
    if not inscripcion_db: raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    inscripcion_db.estudiante_id = inscripcion.estudiante_id
    inscripcion_db.curso_id = inscripcion.curso_id
    inscripcion_db.actualizado_por = username
    await db.commit(); await db.refresh(inscripcion_db); return inscripcion_db

@router.delete("/{inscripcion_id}", summary="Eliminar inscripción")
async def eliminar_inscripcion(inscripcion_id: str, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Inscripcion).where(Inscripcion.id == inscripcion_id))
    inscripcion_db = q.scalars().first()
    if not inscripcion_db: raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    await db.delete(inscripcion_db); await db.commit(); return {"detail": "Inscripción eliminada correctamente"}
