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

@app.put("/profesores/{id}", response_model=Profesor, summary="Actualizar profesor")
def actualizar_Profesor(id: int, profesor: Profesor):
    for i, pr in enumerate(profesores):
        if pr.id == id:
            profesores[i] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="El profesor no fue encontrado")

@app.delete("/profesores/{id}", summary="Eliminar Profesor")
def eliminar_Profesor(id: int):
    for i, pr in enumerate(profesores):
        if pr.id == id:
            profesores.pop(i)
            return {"mensaje": "Profesor Eliminado"}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

# ------------------ CRUD Materia ------------------------ #

@app.get("/materia", response_model=List[Materia], summary="Lista de materias")
def listar_materia():
    return materias

@app.post("/materia", status_code=201, response_model=Materia, summary="Crear Materia")
def crear_materia(materia: Materia):
    for ma in materias:
        if ma.id == materia.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    materias.append(materia)
    return materia


@app.put("/materia/{id}", response_model=Materia, summary="Materia estudiante")
def actualizar_materia(id: int, materia: Materia):
    for i, ma in enumerate(materias):
        if ma.id == id:
            materias[i] = materia
            return materia
    raise HTTPException(status_code=404, detail="La materia no fue encontrado")

@app.delete("/materia/{id}", summary="Eliminar Materia")
def eliminar_materia(id: int):
    for i, ma in enumerate(materias):
        if ma.id == id:
            materias.pop(i)
            return {"mensaje": "Materia Eliminada"}
    raise HTTPException(status_code=404, detail="Materia no encontrada")