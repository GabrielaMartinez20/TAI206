#Importaciones
from fastapi import FastAPI 

#Inicializacion 
app= FastAPI()

#Endpoint
@app.get("/")
async def holamundo():
    return{"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return{"mensaje":"Bienvenidos a tu API REST"}