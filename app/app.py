from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import logging
from loguru import logger
import uvicorn

# Importaciones de controladores
from app.controlador.PatientCrud import GetPatientById, WritePatient, GetPatientByIdentifier
from app.controlador.MedicationCrud import (
    GetmedicationRequestById,
    WritemedicationRequest,
    GetmedicationRequestByIdentifier,
)

## 1. Configuración con variables de entorno
class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    cors_origins: str = "https://frontend-medication-request.onrender.com"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"

settings = Settings()

## 2. Configuración de logging estructurado
logging.basicConfig(level=settings.log_level)
logger.add(
    "app.log",
    rotation="500 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=settings.log_level
)

## 3. Modelos de respuesta
class CreateResponse(BaseModel):
    id: str

## 4. Configuración FastAPI
app = FastAPI(
    title="Healthcare API",
    description="API unificada para gestión de pacientes y medication requests FHIR",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url=None
)

## 5. Configuración CORS segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

## 6. Health Check Endpoint
@app.get("/health", include_in_schema=False)
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy", "version": app.version}

# Endpoints para Pacientes
@app.get("/patient/{patient_id}", 
         response_model=Dict[str, Any],
         status_code=status.HTTP_200_OK,
         responses={
             404: {"description": "Paciente no encontrado"},
             400: {"description": "ID inválido"},
             500: {"description": "Error interno del servidor"}
         })
async def get_patient_by_id(patient_id: str):
    logger.debug(f"Buscando paciente con ID: {patient_id}")
    status_result, patient = GetPatientById(patient_id)
    
    if status_result == 'success':
        logger.info(f"Paciente {patient_id} encontrado")
        return patient
    elif status_result == 'notFound':
        logger.warning(f"Paciente {patient_id} no encontrado")
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found")
    elif status_result == 'invalidId':
        logger.error(f"ID de paciente inválido: {patient_id}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid patient ID format")
    else:
        logger.critical(f"Error inesperado al buscar paciente: {status_result}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal error: {status_result}")

@app.get("/patient/by-identifier", 
         response_model=Dict[str, Any],
         status_code=status.HTTP_200_OK)
async def get_patient_by_identifier(system: str, value: str):
    logger.debug(f"Buscando paciente con identifier: {system}|{value}")
    status_result, patient = GetPatientByIdentifier(system, value)
    
    if status_result == 'success':
        logger.info(f"Paciente encontrado con identifier: {system}|{value}")
        return patient
    elif status_result == 'notFound':
        logger.warning(f"Paciente no encontrado con identifier: {system}|{value}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found with given identifier")
    else:
        logger.error(f"Error al buscar paciente: {status_result}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal error: {status_result}")

@app.post("/patient",
          response_model=CreateResponse,
          status_code=status.HTTP_201_CREATED)
async def add_patient(patient_data: Dict[str, Any]):
    logger.debug("Intentando crear nuevo paciente")
    status_result, patient_id = WritePatient(patient_data)
    
    if status_result == 'success':
        logger.info(f"Nuevo paciente creado con ID: {patient_id}")
        return CreateResponse(id=patient_id)
    else:
        logger.error(f"Error validando paciente: {status_result}")
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Validation error: {status_result}")

# Endpoints para MedicationRequest
@app.get("/medicationRequest/{request_id}", 
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        responses={
            404: {"description": "MedicationRequest no encontrado"},
            400: {"description": "ID inválido"},
            500: {"description": "Error interno del servidor"}
        })
async def get_request_by_id(request_id: str):
    logger.debug(f"Buscando MedicationRequest con ID: {request_id}")
    status_result, medication_request = GetmedicationRequestById(request_id)
    
    if status_result == 'success':
        logger.info(f"MedicationRequest {request_id} encontrado")
        return medication_request
    elif status_result == 'notFound':
        logger.warning(f"MedicationRequest {request_id} no encontrado")
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MedicationRequest not found")
    else:
        logger.error(f"Error al buscar MedicationRequest: {status_result}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal error: {status_result}")

@app.get("/medicationRequest/by-identifier", 
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK)
async def get_request_by_identifier(system: str, value: str):
    logger.debug(f"Buscando MedicationRequest con identifier: {system}|{value}")
    status_result, medication_request = GetmedicationRequestByIdentifier(system, value)
    
    if status_result == 'success':
        logger.info(f"MedicationRequest encontrado con identifier: {system}|{value}")
        return medication_request
    elif status_result == 'notFound':
        logger.warning(f"MedicationRequest no encontrado con identifier: {system}|{value}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MedicationRequest not found with given identifier")
    else:
        logger.error(f"Error al buscar MedicationRequest: {status_result}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal error: {status_result}")

@app.post("/medicationRequest",
         response_model=CreateResponse,
         status_code=status.HTTP_201_CREATED)
async def add_request(request_data: Dict[str, Any]):
    logger.debug("Intentando crear nuevo MedicationRequest")
    status_result, request_id = WritemedicationRequest(request_data)
    
    if status_result == 'success':
        logger.info(f"Nuevo MedicationRequest creado con ID: {request_id}")
        return CreateResponse(id=request_id)
    else:
        logger.error(f"Error validando MedicationRequest: {status_result}")
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Validation error: {status_result}")

# Configuración del servidor
if __name__ == '__main__':
    logger.info(f"Iniciando servidor en {settings.app_host}:{settings.app_port}")
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        log_level=settings.log_level.lower(),
        log_config=None
    )

