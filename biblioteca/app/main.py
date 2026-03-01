#Importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException
import asyncio #importacion de una libreria (time de espera)
from pydantic import BaseModel, Field, constr#libreria pydantic

#Inicializacion 
app= FastAPI(
    title= 'Biblioteca',
    description= 'Gaby Martinez'
)

libros=[
    {"id":1, "nombre":"Odio Odiar", "estado":"prestado","ano":2017, "paginas":194},
    {"id":2, "nombre":"Pensandolo bien, pense mal", "estado":"disponible","ano":2014, "paginas":321},
    {"id":3, "nombre":"It", "estado":"disponible","ano":1986, "paginas":1138},
]

usuarios=[
    {"id":1, "nombre":"Eduardo", "correo":"eduardo_santano.@upq.edu.mx"},
    {"id":2, "nombre":"Rafa", "correo":"rafael_chavez.@upq.edu.mx"},
    {"id":3, "nombre":"Isaac", "correo":"isaac_sanchez.@upq.edu.mx"},
]

prestamos=[
    {"id":1, "id_libro": 1, "id_usuario": 1, "fecha_prestamo": "2026-02-26", "fecha_devolucion": None}
]
#-----------------------------------------------------------------------------------------------------------------------
#Modelo de validacion Pydantic
#----------------------------------------------------------------------------------------------------------------------
class LibroBase(BaseModel):
    id: int = Field(...,gt=0,description="Identificador de libro",example=1)
    nombre: str = Field(...,min_length=3,max_length=100,description="Nombre del libro")
    estado: str = Field(..., pattern='^(disponible|prestado)$', description="Estado del libro")
    ano: int = Field(...,gt=1450,le=2026,description="Año de publicacion")
    paginas: int =Field(...,gt=1,description="Total de paginas del libro")
    
class UsuarioBase(BaseModel):
    nombre: str = Field(...,min_length=3,max_length=50,description="Nombre del usuario")
    correo: str = Field(...,pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Correo de usuario")
    
class PrestamoBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del préstamo", example=1)
    id_libro: int = Field(..., gt=0, description="ID del libro a prestar", example=1)
    id_usuario: int = Field(..., gt=0, description="ID del usuario que solicita", example=1)
    fecha_prestamo: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="Fecha del préstamo (YYYY-MM-DD)", example="2026-02-26")
    fecha_devolucion: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$', description="Fecha de devolución (YYYY-MM-DD)", example="2026-03-26")

#Endpoints
#Registrar un libro
@app.post("/v1/libros", tags=['CRUD libros']) 
async def registarLibros(libro:LibroBase): #Implementamos validacion pydantic
    #Buscar si el id existe
    for lib in libros:
        if lib["id"] == libro.id: 
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
            
    libros.append(libro.dict()) 
    return{
        "mensaje" : "Libro Registrado",
        "datos" : libros,
        "status" : "201"
    }
    
#Listar todos los libros disponibles
@app.get("/v1/libros/disponibles", tags=['CRUD libros'])  
async def consultaLibrosDisponibles():
    libros_disponibles = []
    
    #Buscar libros disponibles
    for lib in libros:
        if lib["estado"] == "disponible":
            libros_disponibles.append(lib)
    
    return {
        "status": "200",
        "total": len(libros_disponibles),
        "data": libros_disponibles
    }
    
#Buscar un libro por su nombre
@app.get("/v1/libros/{nombre}", tags=['CRUD libros'])
async def consultaLibro(nombre: str):
    # Buscar el libro por nombre
    for lib in libros:
        if lib["nombre"].lower() == nombre.lower():  # Comparación sin distinguir mayúsculas
            return {
                "mensaje": "Libro encontrado",
                "datos": lib,
                "status": "200"
            }
    
    # Si no se encuentra el libro
    raise HTTPException(
        status_code=404,
        detail=f"El libro '{nombre}' no existe"
    )

#Registrar el préstamo de un libro a un usuario
@app.post("/v1/prestamos", tags=['CRUD Préstamos'])
async def registrarPrestamo(prestamo: PrestamoBase):
    # Verificar que el ID del préstamo no exista
    for p in prestamos:
        if p["id"] == prestamo.id:
            raise HTTPException(
                status_code=400,
                detail="El ID del préstamo ya existe"
            )
    
    # Verificar que el libro exista
    libro_existe = False
    for lib in libros:
        if lib["id"] == prestamo.id_libro:
            libro_existe = True
            # Verificar que el libro esté disponible
            if lib["estado"] != "disponible":
                raise HTTPException(
                    status_code=409,
                    detail=f"El libro '{lib['nombre']}' no está disponible (estado: {lib['estado']})"
                )
            break
    
    if not libro_existe:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el libro con ID: {prestamo.id_libro}"
        )
    
    # Verificar que el usuario exista
    usuario_existe = False
    for user in usuarios:
        if user["id"] == prestamo.id_usuario:
            usuario_existe = True
            break
    
    if not usuario_existe:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el usuario con ID: {prestamo.id_usuario}"
        )
    
    #Actualizar el estado del libro a "prestado"
    for lib in libros:
        if lib["id"] == prestamo.id_libro:
            lib["estado"] = "prestado"
            break
    
    #Agregar el préstamo
    prestamos.append(prestamo.model_dump())
    
    return {
        "mensaje": "Préstamo registrado exitosamente",
        "datos": prestamo.model_dump(),
        "status": "201"
    }
                                                                                                                                          
#Marcar un libro como devuelto
@app.put("/v1/prestamos/{id_prestamo}/devolucion", tags=['CRUD Préstamos'])
async def marcarComoDevuelto(id_prestamo: int):

    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            # Cambiar el estado del libro a disponible
            for lib in libros:
                if lib["id"] == prestamo["id_libro"]:
                    lib["estado"] = "disponible"
                    break
            
            return {
                "mensaje": "Libro marcado como devuelto",
                "datos": prestamo,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Préstamo no encontrado"
    )
    
#Eliminar el registro de un préstamo
@app.delete("/v1/prestamos/{id_prestamo}", tags=['CRUD Préstamos'])
async def eliminarPrestamo(id_prestamo: int):
    #Buscar prestamo
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            # Verificar si el libro ya fue devuelto
            if prestamo["fecha_devolucion"] is None:
                # Si no se ha devuelto, cambiar el estado del libro a disponible
                for lib in libros:
                    if lib["id"] == prestamo["id_libro"]:
                        lib["estado"] = "disponible"
                        break
            
            # Eliminar el préstamo usando remove()
            prestamos.remove(prestamo)
            
            return {
                "mensaje": "Préstamo eliminado exitosamente",
                "datos": prestamo,
                "status": "200"
            }
    
    # Si no se encuentra el préstamo
    raise HTTPException(
        status_code=409,
        detail=f"No existe el préstamo con ID: {id_prestamo}"
    )
        