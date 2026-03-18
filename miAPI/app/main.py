#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc


#Inicializacion 
app= FastAPI(
    title= 'Mi primer API',
    description= 'Gaby Martinez',
    version= '1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)