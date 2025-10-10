from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Apis.routes import ALL_ROUTERS

app = FastAPI(title="API Escuela - Proyecto Final")

# --- Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta a tus dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registro automático de rutas
for r in ALL_ROUTERS:
    app.include_router(r)

@app.get("/")
def root():
    return {"message": "API Web Escuela funcionando correctamente 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
