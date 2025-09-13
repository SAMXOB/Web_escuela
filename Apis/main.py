from fastapi import FastAPI
from Apis.estudiantes import router as estudiantes_router
from Apis.profesores import router as profesores_router
from Apis.materias import router as materias_router

app = FastAPI(title="API Escuela - Parcial 1")

app.include_router(estudiantes_router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(profesores_router, prefix="/profesores", tags=["Profesores"])
app.include_router(materias_router, prefix="/materias", tags=["Materias"])

