from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, func

from ..auth import create_access_token
from ..deps import get_db
from ..models import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", summary="Autenticación de usuario")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Permitir username o email
    stmt = select(Usuario).where(
        or_(
            func.lower(Usuario.username) == func.lower(form_data.username),
            func.lower(Usuario.email) == func.lower(form_data.username),
        )
    )
    q = await db.execute(stmt)
    user = q.scalars().first()

    if not user:
        # 404 para distinguir "no existe" de "password incorrecto"
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # OJO: esto compara en texto plano (útil para pruebas)
    # Para producción usa bcrypt.verify(...)
    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
