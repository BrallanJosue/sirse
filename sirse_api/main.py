from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from . import models
import os

# Routers
from .routers import auth, categorias, estados, reportes, estadisticas, usuarios


# ========= CREAR TABLAS (solo local) =========
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass


# ========= CONFIG APP =========
app = FastAPI(
    title="SIRSE API",
    description="Sistema Integral de Reportes de Seguridad y Emergencias",
    version="1.0.0"
)


# ========= CORS =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========= ARCHIVOS ESTÁTICOS (panel admin en local) =========
# Solo funciona si ejecutas FastAPI localmente.
# En Vercel se sirve desde vercel.json
PANEL_PATH = os.path.join(os.path.dirname(__file__), "..", "sirse-admin-panel")

if os.path.isdir(PANEL_PATH):
    app.mount("/", StaticFiles(directory=PANEL_PATH, html=True), name="static")


# ========= ROUTERS =========
app.include_router(auth.router)
app.include_router(categorias.router, prefix="/api", tags=["categorias"])
app.include_router(estados.router, prefix="/api", tags=["estados"])
app.include_router(reportes.router, prefix="/api", tags=["reportes"])
app.include_router(estadisticas.router, prefix="/api", tags=["estadisticas"])
app.include_router(usuarios.router, prefix="/api", tags=["usuarios"])


# ========= RUTAS BÁSICAS =========
@app.get("/", tags=["root"])
def root():
    return {
        "message": "Bienvenido a SIRSE API",
        "version": "1.0.0",
        "docs": "/docs",
        "sistema": "Sistema Integral de Reportes de Seguridad y Emergencias"
    }


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "SIRSE API"}


# ========= EJECUCIÓN LOCAL =========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
