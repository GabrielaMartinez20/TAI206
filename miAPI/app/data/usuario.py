#Modelo para la base de datos 
#Importaciones 
from sqlalchemy import Column, Integer, String
from app.data.db import Base

#Modelo para trabajar las operaciones
class Usuario(Base):
    __tablename__ ="tb_usuarios"
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)
    