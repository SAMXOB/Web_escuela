from fastapi import HTTPException,APIRouter
from typing import List, Optional
from Apis.models import  Materia
from Apis.data import  materias

router = APIRouter()
# ------------------ CRUD Materia ------------------------ #

@router.get("/materia", response_model=List[Materia], summary="Lista de materias")
def listar_materia():
    return materias

@router.get("/materia/{id}", response_model=Materia, summary="Obtener materia por ID")
def obtener_materia(id: int):
    for mat in materias:
        if mat.id == id:
            return mat
    raise HTTPException(status_code=404, detail="Materia no encontrada")

@router.post("/materia", status_code=201, response_model=Materia, summary="Crear Materia")
def crear_materia(materia: Materia):
    for ma in materias:
        if ma.id == materia.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    materias.routerend(materia)
    return materia


@router.put("/materia/{id}", response_model=Materia, summary="Materia estudiante")
def actualizar_materia(id: int, materia: Materia):
    for i, ma in enumerate(materias):
        if ma.id == id:
            materias[i] = materia
            return materia
    raise HTTPException(status_code=404, detail="La materia no fue encontrado")

@router.delete("/materia/{id}", summary="Eliminar Materia")
def eliminar_materia(id: int):
    for i, ma in enumerate(materias):
        if ma.id == id:
            materias.pop(i)
            return {"mensaje": "Materia Eliminada"}
    raise HTTPException(status_code=404, detail="Materia no encontrada")