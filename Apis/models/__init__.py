from sqlalchemy.orm import declarative_base

# Declarar la base para todos los modelos
Base = declarative_base()

# Importar todos los modelos para que se registren en la metadata
from .usuario import *
from .estudiante import *
from .profesor import *
from .materia import *
from .curso import *
from .inscripcion import *
