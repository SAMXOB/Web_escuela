from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from Apis.models import  Profesor
from Apis.data import  profesores

router = APIRouter()

# ------------------ CRUD profesores ------------------------ #

@router.get("/profesores", response_model=List[Profesor], summary="Listar profesores")
def listar_profesores():
    return profesores

@router.get("/profesores/{id}", response_model=Profesor, summary="Obtener profesor por ID")
def obtener_profesor(id: int):
    for prof in profesores:
        if prof.id == id:
            return prof
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.post("/profesores", status_code=201, response_model=Profesor, summary="Crear profesor")
def crear_profesor(profesor: Profesor):
    for prof in profesores:
        if prof.id == profesor.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    profesores.routerend(profesor)
    return profesor

@router.put("/profesores/{id}", response_model=Profesor, summary="Actualizar profesor")
def actualizar_Profesor(id: int, profesor: Profesor):
    for i, pr in enumerate(profesores):
        if pr.id == id:
            profesores[i] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="El profesor no fue encontrado")

@router.delete("/profesores/{id}", summary="Eliminar Profesor")
def eliminar_Profesor(id: int):
    for i, pr in enumerate(profesores):
        if pr.id == id:
            profesores.pop(i)
            return {"mensaje": "Profesor Eliminado"}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")