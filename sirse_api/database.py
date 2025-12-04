from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env local, Vercel usa env internos)
load_dotenv()

# ==========================================
# 1) CONFIG VERCEL → PostgreSQL
# ==========================================
POSTGRES_URL = os.getenv("POSTGRES_URL")

# ==========================================
# 2) CONFIG LOCAL → MySQL
# ==========================================
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "sirse")

if not DB_PORT or DB_PORT == "None":
    DB_PORT = "3306"

MYSQL_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================
# 3) SELECCIONAR AUTOMÁTICAMENTE LA BD
# ==========================================
if POSTGRES_URL:
    # Vercel
    DATABASE_URL = POSTGRES_URL
    print("▶ Usando PostgreSQL (Vercel)")
else:
    # Local
    DATABASE_URL = MYSQL_URL
    print("▶ Usando MySQL local")

print(f"Conexión a BD: {DATABASE_URL}")

# ==========================================
# 4) INICIALIZACIÓN DEL MOTOR
# ==========================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Cambia a True si quieres ver las consultas SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ==========================================
# 5) Dependencia de BD
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
