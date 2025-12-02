"""
Script para poblar la base de datos con datos iniciales
Ejecutar con: python -m sirse_api.seed_data
"""
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Categoria, Estado, Departamento, Base
from datetime import datetime

def init_db():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos en ESTADOS
        if db.query(Estado).count() > 0:
            print("⚠️  Ya existen datos en la base de datos")
            print("📊 Resumen de datos existentes:")
            print(f"   - Estados: {db.query(Estado).count()}")
            print(f"   - Categorías: {db.query(Categoria).count()}")
            print(f"   - Departamentos: {db.query(Departamento).count()}")
            return
        
        print("🔄 Creando datos iniciales...")
        
        # ============= CREAR ESTADOS =============
        estados = [
            Estado(
                nombre="Pendiente", 
                descripcion="Reporte recibido, pendiente de revisión", 
                activo=True
            ),
            Estado(
                nombre="En proceso", 
                descripcion="Reporte en proceso de atención", 
                activo=True
            ),
            Estado(
                nombre="Resuelto", 
                descripcion="Reporte atendido y resuelto", 
                activo=True
            ),
            Estado(
                nombre="Rechazado", 
                descripcion="Reporte no válido o duplicado", 
                activo=True
            ),
            Estado(
                nombre="Cerrado", 
                descripcion="Reporte cerrado", 
                activo=True
            ),
        ]
        
        db.add_all(estados)
        db.commit()
        print("✅ Estados creados correctamente")
        
        # ============= CREAR CATEGORÍAS =============
        categorias = [
            Categoria(
                nombre="Seguridad", 
                descripcion="Reportes relacionados con seguridad pública", 
                estado=True
            ),
            Categoria(
                nombre="Robo", 
                descripcion="Reportes de robos o asaltos", 
                estado=True
            ),
            Categoria(
                nombre="Accidente", 
                descripcion="Reportes de accidentes viales", 
                estado=True
            ),
            Categoria(
                nombre="Vandalismo", 
                descripcion="Actos de vandalismo o daños a propiedad", 
                estado=True
            ),
            Categoria(
                nombre="Persona sospechosa", 
                descripcion="Reportes de personas con actitud sospechosa", 
                estado=True
            ),
            Categoria(
                nombre="Alumbrado público", 
                descripcion="Problemas con iluminación en vías públicas", 
                estado=True
            ),
            Categoria(
                nombre="Baches", 
                descripcion="Reportes de baches en calles", 
                estado=True
            ),
            Categoria(
                nombre="Basura", 
                descripcion="Acumulación de basura o residuos", 
                estado=True
            ),
            Categoria(
                nombre="Fuga de agua", 
                descripcion="Reportes de fugas de agua", 
                estado=True
            ),
            Categoria(
                nombre="Animal callejero", 
                descripcion="Presencia de animales en la vía pública", 
                estado=True
            ),
            Categoria(
                nombre="Otro", 
                descripcion="Otros tipos de reportes", 
                estado=True
            ),
        ]
        
        db.add_all(categorias)
        db.commit()
        print("✅ Categorías creadas correctamente")
        
        # ============= CREAR DEPARTAMENTOS =============
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
        
        print("\n" + "="*50)
        print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*50)
        print(f"📊 RESUMEN DE DATOS CREADOS:")
        print(f"   📋 {len(estados)} estados")
        print(f"   🏷️  {len(categorias)} categorías")
        print(f"   🏛️  {len(departamentos)} departamentos")
        print("="*50)
        print("\n📍 Los departamentos disponibles son:")
        for i, depto in enumerate(departamentos, 1):
            print(f"   {i}. {depto.nombre} - {depto.descripcion}")
        
    except Exception as e:
        print(f"\n❌ ERROR al inicializar la base de datos:")
        print(f"   Mensaje: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 INICIALIZANDO BASE DE DATOS SIRSE...")
    print("📍 Municipio de Tulancingo de Bravo")
    print("="*50)
    init_db()