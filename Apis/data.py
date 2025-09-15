from Apis.models import Estudiante, Profesor, Materia

estudiantes = [
    Estudiante(id=1, nombre="Ana", apellido="Gomez", email="ana@example.com", materias=[1,2]),
    Estudiante(id=2, nombre="Luis", apellido="Martínez", email="luis@example.com", materias=[2])
]

profesores = [
    Profesor(id=1, nombre="Carlos", apellido="Ruiz", email="carlos@example.com", materia_id=1)
]

materias = [
    Materia(id=1, nombre="Matemáticas", creditos=3, profesor_id=1),
    Materia(id=2, nombre="Historia", creditos=2)
]