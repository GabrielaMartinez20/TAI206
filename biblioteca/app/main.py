#Importaciones 
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio #importacion de una libreria (time de espera)
from pydantic import BaseModel, Field, field_validator #libreria pydantic
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date, datetime

#Inicializacion 
app= FastAPI(
    title= 'Examen',
    description= 'Gaby Martinez',
    
)

#Modelo pydantic
citas = [
    {"id":1, "paciente":"Gabis", "fecha":"2026-03-10", "motivo":"Dolor de cabeza", "confirmar":"True"},
    {"id":2, "paciente":"Isaac", "fecha":"2026-03-12", "motivo":"Dolor de estomago", "confirmar":"False"},
    {"id":3, "paciente":"Ana Laura", "fecha":"2026-03-15", "motivo":"gripe frecuente", "confirmar":"True"},
]

#Modelo de validacion Pydantic
class CitaBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de cita",example="1")
    paciente: str = Field(...,min_length=5,max_length=50,description="Nombre del paciente")
    fecha: date = Field(..., description="Fecha de la cita (YYYY-MM-DD)")
    motivo: str = Field(...,min_length=8,max_length=100,description="Motivo de la cita")
    confirmar: bool = Field(False, description="Confirmación de cita")
    
@field_validator('fecha')
def validar_fecha(cls, v):
    if v < date.today():
        raise ValueError('Revisar fecha ingresada')
    return v
    
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
        "data": citas
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
    for cit in citas:
        if cit["id"] == id: 
            return{"Cita encontrada": id, 
               "datos": cit,  
               "status" : "200"}
    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )

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
    

