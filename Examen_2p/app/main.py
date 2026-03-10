#Importaciones 
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio #importacion de una libreria (time de espera)
from pydantic import BaseModel, Field #libreria pydantic
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Inicializacion 
app= FastAPI(
    title= 'Examen',
    description= 'Gaby Martinez',
    
)

#Modelo pydantic
citas = [
    {"id":1, "paciente":"Gabis", "fecha":"10-03-2026", "motivo":"Dolor de cabeza", "confirmacion":"1"},
    {"id":2, "paciente":"Isaac", "fecha":"12-03-2026", "motivo":"Dolor de estomago", "confirmacion":"0"},
    {"id":1, "paciente":"Ana Laura", "fecha":"15-03-2026", "motivo":"gripe frecuente", "confirmacion":"1"},
]

#Modelo de validacion Pydantic
class CitaBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de cita",example="1")
    paciente: str = Field(...,min_length=5,max_length=50,description="Nombre del paciente")
    fecha:int = Field(...,ge=0,le=121,description="fecha de la cita")
    motivo: str = Field(...,min_length=8,max_length=100,description="Motivo de la cita")
    confirmar: int = Field(...,ge=0,le=1,description="Confirmacion de cita")
    
#Seguridad
security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials= Depends(security)):
    usuarioAuth=secrets.compare_digest(credentials.username,"root")
    contraAuth=secrets.compare_digest(credentials.password,"1234")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Crendenciales no validas"
        )
    return credentials.username    

#Endpoints
#Listar citas 
@app.get("/v1/citas", tags=['CRUD'])
async def listarCita(usuarioAuth: str= Depends(verificar_Peticion)): 
    return{
        "status":"200",
        "total": len(citas),
        "data":citas
    }
 
#Crear citas
@app.post("/v1/cita", tags=['CRUD'])
async def agregarCita(cita:CitaBase): 
    for cit in citas:
        if cit["id"] == cita.id: 
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
            
    citas.append(cita)
    return{
        "mensaje" : "Cita Agregada",
        "datos" : cita,
        "status" : "200"
    }

#Consultar por ID
@app.get("/v1/cita/{id}", tags=['CRUD'])
async def consultaCita(id:int):
    return{"Cita encontrada":id}

#Confirmar citas 
@app.put("/v1/cita/{id}", tags=['CRUD'])
async def actualizarCita(id: int, cita: dict):
    for cit in citas:
        if cit["id"] == id:
            cit.update(cita)
            return {
                "mensaje": "Cita actualizada",
                "datos": cit,
                "status": 200
            }
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

#eliminar citas
@app.delete("/v1/cita/{id}", tags=['CRUD'])
async def eliminarCita(id: int, usuarioAuth: str= Depends(verificar_Peticion)):
    for cit in citas:
        if cit["id"] == id:
            citas.remove(cit)
            return{
                "mensaje": "Cita eliminada",
                "datos": cit,
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada para eliminar"
    )
    

