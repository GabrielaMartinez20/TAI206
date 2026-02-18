#Importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException
import asyncio #importacion de una libreria (time de espera)
from pydantic import BaseModel, Field #libreria pydantic

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
#Modelo de validacion Pydantic
class UauarioBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de usuario",example="1")
    nombre: str = Field(...,min_length=3,max_length=50,description="Nombre del usuario")
    edad:int = Field(...,ge=0,le=121,description="Edad validada entre 0 y 121")

#Endpoint
@app.get("/", tags=['Inicio'])
async def holamundo():
    return{"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return{"mensaje":"Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return{"mensaje":"Tu calificacion en TAI es 10"}

@app.get("/v1/parametroO/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuario(id:int):
    return{"Usuario encontrado":id}

@app.get("/v1/parametroOp", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"}
    
@app.get("/v1/usuarios", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
    
@app.post("/v1/usuarios", tags=['CRUD usuarios'])
async def agregarUsuarios(usuario:UauarioBase): #Borramos diccionarios, implementamos validadcion pydantic
    for usr in usuarios:
        if usr["id"] == usuario.id: #modificamos por el cambio de diccionario
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
            
    usuarios.append(usuario)
    return{
        "mensaje" : "Usuario Agregado",
        "datos" : usuario,
        "status" : "200"
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def actualizarUsuario(id: int, usuario: dict):

    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return {
                "mensaje": "Usuario actualizado",
                "datos": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def eliminarUsuario(id: int):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado",
                "datos": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para eliminar"
    )
  