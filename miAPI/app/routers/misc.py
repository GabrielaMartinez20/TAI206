#********************************************
# Otros endpoints
#********************************************

#Importaciones 
from fastapi import APIRouter
from typing import Optional
import asyncio #importacion de una libreria (time de espera)
from app.data.database import usuarios

router = APIRouter(tags=["Varios"])

@router.get("/")
async def holamundo():
    return{"mensaje":"Hola mundo FastAPI"}

@router.get("/v1/bienvenidos")
async def bienvenido():
    return{"mensaje":"Bienvenidos a tu API REST"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(6)
    return{"mensaje":"Tu calificacion en TAI es 10"}

@router.get("/v1/parametroO/{id}")
async def consultaUsuario(id:int):
    return{"Usuario encontrado":id}

@router.get("/v1/parametroOp")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"}
    
