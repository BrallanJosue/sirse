"""
Script para agregar solo departamentos
"""
from sqlalchemy.orm import Session
from sirse_api.database import SessionLocal
from sirse_api.models import Departamento
from datetime import datetime

def seed_departamentos():
    db = SessionLocal()
    
    try:
        # Verificar si ya hay departamentos
        count = db.query(Departamento).count()
        if count > 0:
            print(f"⚠️  Ya existen {count} departamentos en la base de datos")
            print("📋 Lista de departamentos existentes:")
            departamentos = db.query(Departamento).all()
            for depto in departamentos:
                print(f"   - {depto.nombre}")
            return
        
        print("🔄 Agregando departamentos...")
        
        departamentos = [
            Departamento(
                nombre="Alumbrado Público", 
                descripcion="Mantenimiento de alumbrado público y luminarias",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Servicios Municipales", 
                descripcion="Servicios generales y atención ciudadana",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Parques y Jardines", 
                descripcion="Mantenimiento de áreas verdes y espacios públicos",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Obras Públicas", 
                descripcion="Construcción y mantenimiento de infraestructura urbana",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Seguridad Pública", 
                descripcion="Protección y seguridad ciudadana",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Protección Civil", 
                descripcion="Emergencias y protección civil",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Tránsito y Vialidad", 
                descripcion="Control de tránsito y mantenimiento vial",
                activo=True,
                created_at=datetime.now()
            ),
            Departamento(
                nombre="Desarrollo Urbano", 
                descripcion="Planificación y desarrollo urbano",
                activo=True,
                created_at=datetime.now()
            ),
        ]
        
        db.add_all(departamentos)
        db.commit()
        
        print("✅ Departamentos creados correctamente")
        print(f"📊 Total: {len(departamentos)} departamentos")
        print("\n📍 Departamentos creados:")
        for i, depto in enumerate(departamentos, 1):
            print(f"   {i}. {depto.nombre}")
            
    except Exception as e:
        print(f"❌ Error al crear departamentos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 AGREGANDO DEPARTAMENTOS A LA BASE DE DATOS...")
    seed_departamentos()