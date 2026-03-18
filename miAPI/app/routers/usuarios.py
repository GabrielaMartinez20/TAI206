#*************************************************************
# Usuarios CRUD
#*************************************************************
#importaciones 
from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UauarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD HTTP"]
)

#Endpoints
@router.get("/")
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregarUsuarios(usuario:UauarioBase): #Implementamos validadcion pydantic
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje" : "Usuario Agregado",
        "datos" : usuario
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
  