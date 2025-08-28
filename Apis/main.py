from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from models import Estudiante, Profesor, Materia
from data import estudiantes, profesores, materias

app = FastAPI(title="API Escuela - Parcial 1")

#------------------ CRUD Estudiantes -----------------#

@app.get("/estudiantes", response_model=List[Estudiante], summary="Listar Estudiantes")
def listar_estudiantes(materia_id: Optional[int] = Query(None, description="Filtrar por materia")):
    if materia_id is not None:
        return[est for est in estudiantes if materia_id in est.materias]
    return estudiantes

@app.get("/estudiantes/{id}", response_model=Estudiante, summary="Obtener estudiante por ID")
def obtener_estudiante(id: int):
    for est in estudiantes:
        if est.id == id:
            return est
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@app.post("/estudiantes", status_code=201, response_model=Estudiante, summary="Crear estudiante")
def crear_estudiante(estudiante: Estudiante):
    for est in estudiantes:
        if est.id == estudiante.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    estudiantes.append(estudiante)
    return estudiante

@app.put("/estudiantes/{id}", response_model=Estudiante, summary="Actualizar estudiante")
def actualizar_estudiante(id: int, estudiante: Estudiante):
    for i, est in enumerate(estudiantes):
        if est.id == id:
            estudiantes[i] = estudiante
            return estudiante
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@app.delete("/estudiantes/{id}", summary="Eliminar estudiante")
def eliminar_estudiante(id: int):
    for i, est in enumerate(estudiantes):
        if est.id == id:
            estudiantes.pop(i)
            return {"mensaje": "Estudiante eliminado"}
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")
# ------------------ CRUD profesores ------------------------ #

@app.get("/profesores", response_model=List[Profesor], summary="Listar profesores")
def listar_profesores():
    return profesores

@app.post("/profesores", status_code=201, response_model=Profesor, summary="Crear profesor")
def crear_profesor(profesor: Profesor):
    for prof in profesores:
        if prof.id == profesor.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    profesores.append(profesor)
    return profesor