from .auth_routes import router as auth_router
from .usuarios_routes import router as usuarios_router
from .estudiantes_routes import router as estudiantes_router
from .profesores_routes import router as profesores_router
from .materias_routes import router as materias_router
from .cursos_routes import router as cursos_router
from .inscripciones_routes import router as inscripciones_router

ALL_ROUTERS = [
    auth_router,
    usuarios_router,
    estudiantes_router,
    profesores_router,
    materias_router,
    cursos_router,
    inscripciones_router,
]
