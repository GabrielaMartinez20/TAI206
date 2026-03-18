#*****************************
#SEGURIDAD CON HTTP BASIC
#****************************
#Importaciones 
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials= Depends(security)):
    usuarioAuth=secrets.compare_digest(credentials.username,"admin")
    contraAuth=secrets.compare_digest(credentials.password,"1234")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Crendenciales no validas"
        )
    return credentials.username    