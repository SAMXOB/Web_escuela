from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from ..deps import get_db
from ..models import  Materia
from Apis.schemas import MateriaCreate, MateriaResponse

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("", response_model=List[MateriaResponse], summary="Listar materias")
async def listar_materias(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    res = await db.execute(select(Materia)); return res.scalars().all()

@router.post("", response_model=MateriaResponse, summary="Crear materia")
async def crear_materia(materia: MateriaCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    nueva = Materia(nombre=materia.nombre, creditos=materia.creditos, profesor_id=materia.profesor_id,
                    creado_por=username, actualizado_por=username)
    db.add(nueva); await db.commit(); await db.refresh(nueva); return nueva

@router.put("/{materia_id}", response_model=MateriaResponse, summary="Actualizar materia")
async def actualizar_materia(materia_id: str, materia: MateriaCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Materia).where(Materia.id == materia_id))
    materia_db = q.scalars().first()
    if not materia_db: raise HTTPException(status_code=404, detail="Materia no encontrada")
    materia_db.nombre = materia.nombre; materia_db.creditos = materia.creditos
    materia_db.profesor_id = materia.profesor_id; materia_db.actualizado_por = username
    await db.commit(); await db.refresh(materia_db); return materia_db

@router.delete("/{materia_id}", summary="Eliminar materia")
async def eliminar_materia(materia_id: str, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Materia).where(Materia.id == materia_id))
    materia_db = q.scalars().first()
    if not materia_db: raise HTTPException(status_code=404, detail="Materia no encontrada")
    await db.delete(materia_db); await db.commit(); return {"detail": "Materia eliminada correctamente"}
