#  IMPORTACIONES 
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import jwt 
from datetime import datetime, timedelta, timezone

# Inicializacion
app = FastAPI(
    title="My API", 
    description="Gabriela Martinez",
    version="2.0"
)

users = [
    {"id": 1, "name": "Gabi Martinez", "age": 20, "alias": "Gabi"},
    {"id": 2, "name": "Isaac Sanchez", "age": 22, "alias": "friend"},
    {"id": 3, "name": "David Santiago", "age": 21, "alias": "bomba"},
]

# Modelo de validacion Pydantic
class UserBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example=1)
    name: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    age: int = Field(..., ge=0, le=121, description="Edad validada entre 0 y 121")
    aka: str = Field(..., min_length=3, max_length=50, description="Alias del usuario", example="The best")   

#************************************
#  Seguridad con OAUTH2/JWT
#************************************
SECRET_KEY = "secreto_para_firmar_tokens" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define el esquema OAuth2 y la ruta donde el cliente pedirá el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crear_token_acceso(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decodificamos el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


# endpoints
# ENDPOINT PARA GENERAR TOKEN 
@app.post("/token", tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "gabi" or form_data.password != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generar token si es exitoso
    tiempo_expiracion = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_generado = crear_token_acceso(
        data={"sub": form_data.username}, expires_delta=tiempo_expiracion
    )
    return {"access_token": token_generado, "token_type": "bearer"}

@app.get("/", tags=["Start"])
async def helloworld(): return {"message": "Hello world FastAPI"}

@app.get("/v1/welcome_message", tags=["Start"])
async def welcome_message(): return {"message": "Welcome to your API REST"}

@app.get("/v1/grades", tags=["Asynchrony"])
async def grades():
    await asyncio.sleep(5)
    return {"message": "Your grade in TAI is 10"}

@app.get("/v1/user/{id}", tags=["Required_parameter"])
async def user(id: int):
    await asyncio.sleep(3)
    return {"user_found": id}

@app.get("/v1/user_optional/", tags=["Optional_parameter"])
async def user_optional(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for user in users:
            if user["id"] == id: return {"user": user}
        return {"message": "Usuario no encontrado"}
    return {"message": "No se proporciono id"}

@app.get("/v1/users", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return {"status": "200", "total": len(users), "data": users}

@app.post("/v1/users", tags=['CRUD usuarios'])
async def add_usuers(user: UserBase):
    for usr in users:
        if usr["id"] == user.id: raise HTTPException(status_code=400, detail="El id ya existe")
    users.append(user.dict())
    return {"message": "Usuario agregado correctamente", "datos": user, "status": "200"}


@app.put("/v1/users/{id}", tags=['CRUD usuarios'])
async def update_user(id: int, user_updated: dict, current_user: str = Depends(validar_token)):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            user_updated["id"] = id 
            users[index] = user_updated
            return {"message": f"Usuario actualizado por {current_user}", "datos": user_updated}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para actualizar")


@app.delete("/v1/users/{id}", tags=['CRUD usuarios'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user: str = Depends(validar_token)):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            users.pop(index) 
            return None 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar")