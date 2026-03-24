#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuario

#Crea la tabla sino existe
usuario.Base.metadata.create_all(bind=engine)


#Inicializacion 
app= FastAPI(
    title= 'Mi primer API',
    description= 'Gaby Martinez',
    version= '1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)