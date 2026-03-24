#Importaciones 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. definiendo la URL de conexion
DATABASE_URL= os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. creamos el motor de conexion 
engine= create_engine(DATABASE_URL)

#3. Agregamos el gestor de sesiones 
sesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

#4. Base declarativa para modelos
Base= declarative_base()

#5. funcion para el manejo en session en los request
def get_db():
    db = sesionLocal()
    try:
        yield db
    finally:
        db.close()
