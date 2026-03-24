#*************************************************************
# Usuarios CRUD
#*************************************************************
#importaciones 
from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

#Importaciones para usar los endpoints
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD HTTP"]
)

#Endpoints
@router.get("/")
async def consultaUsuarios(db:Session = Depends(get_db)):
    consultausuarios=db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(consultausuarios),
        "data":consultausuarios
    }
    
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregarUsuarios(usuarioP:UsuarioBase, db:Session=Depends(get_db)): #Implementamos validadcion pydantic
    
    nuevoUsuario = usuarioDB(nombre= usuarioP.nombre, edad=usuarioP.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    
    return{
        "mensaje" : "Usuario Agregado",
        "datos" : nuevoUsuario
    }
    
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizarUsuario(id: int, usuario: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            #Remplazamos completamente el usuario
            usuario["id"] = id
            usuarios[index]=usuario
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuarios[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminarUsuario(id: int, usuarioAuth: str= Depends(verificar_Peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para eliminar"
    )
  