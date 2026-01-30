#Importaciones
from typing import Optional
from fastapi import FastAPI 
import asyncio #importacion de una libreria (time de espera)

#Inicializacion 
app= FastAPI(
    title= 'Mi primer API',
    description= 'Gaby Martinez',
    version= '1.0'
)

usuarios=[
    {"id":1, "nombre":"Gabi", "edad":23},
    {"id":2, "nombre":"Rafa", "edad":25},
    {"id":3, "nombre":"Isaac", "edad":22},
]

#Endpoint
@app.get("/", tags={'Inicio'})
async def holamundo():
    return{"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos", tags={'Inicio'})
async def bienvenido():
    return{"mensaje":"Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones", tags={'Asincronia'})
async def calificaciones():
    await asyncio.sleep(6)
    return{"mensaje":"Tu calificacion en TAI es 10"}

@app.get("/v1/usuarios/{id}", tags={'Parametro Obligatorio'})
async def consultaUsuario(id:int):
    await asyncio.sleep(3)
    return{"Usuario encontrado":id}

@app.get("/v1/usuarios_op/{id}", tags={'Parametro Opcional'})
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"}