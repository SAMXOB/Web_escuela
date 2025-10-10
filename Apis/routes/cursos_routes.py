from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Apis.auth import verify_token
from ..deps import get_db
from ..models import  Curso
from Apis.schemas import CursoCreate, CursoResponse

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("", response_model=List[CursoResponse], summary="Listar cursos")
async def listar_cursos(db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    res = await db.execute(select(Curso)); return res.scalars().all()

@router.post("", response_model=CursoResponse, summary="Crear curso")
async def crear_curso(curso: CursoCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    nuevo = Curso(nombre=curso.nombre, materia_id=curso.materia_id,
                  creado_por=username, actualizado_por=username)
    db.add(nuevo); await db.commit(); await db.refresh(nuevo); return nuevo

@router.put("/{curso_id}", response_model=CursoResponse, summary="Actualizar curso")
async def actualizar_curso(curso_id: str, curso: CursoCreate, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso_db = q.scalars().first()
    if not curso_db: raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_db.nombre = curso.nombre; curso_db.materia_id = curso.materia_id
    curso_db.actualizado_por = username
    await db.commit(); await db.refresh(curso_db); return curso_db

@router.delete("/{curso_id}", summary="Eliminar curso")
async def eliminar_curso(curso_id: str, db: AsyncSession = Depends(get_db), username: str = Depends(verify_token)):
    q = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso_db = q.scalars().first()
    if not curso_db: raise HTTPException(status_code=404, detail="Curso no encontrado")
    await db.delete(curso_db); await db.commit(); return {"detail": "Curso eliminado correctamente"}
