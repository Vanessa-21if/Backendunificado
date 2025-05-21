from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://21vanessaaa:VANEifmer2025@sampleinformationservic.ceivw.mongodb.net/?retryWrites=true&w=majority&appName=SampleInformationService"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ConfigurationError
import logging
from typing import Union
from pydantic import BaseSettings

# Configuración mediante variables de entorno
class MongoDBSettings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://21vanessaaa:VANEifmer2025@sampleinformationservic.ceivw.mongodb.net/?retryWrites=true&w=majority&appName=SampleInformationService"
    MONGO_DB_NAME: str = "EntregaDeMedicamentos"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = MongoDBSettings()

def connect_to_mongodb(db_name: str = None, collection_name: str = None) -> Union[MongoClient, 'Collection']:
    """
    Establece conexión segura con MongoDB y retorna la colección especificada
    
    Args:
        db_name: EntregaDeMdicamentos
        collection_name: medicationRequest
    
    Returns:
        MongoClient si no se especifica db_name y collection_name
        Collection si se especifican ambos
        
    Raises:
        ConnectionFailure: Si no se puede conectar al servidor
        ConfigurationError: Si hay problemas con la URI de conexión
    """
    try:
        # Configuración de conexión segura
        client = MongoClient(
            settings.MONGO_URI,
            server_api=ServerApi('1'),
            connectTimeoutMS=5000,
            socketTimeoutMS=3000,
            serverSelectionTimeoutMS=5000
        )
        
        # Verificar conexión
        client.admin.command('ping')
        logging.info("Conexión exitosa a MongoDB")
        
        # Retornar cliente si no se especifica colección
        if not db_name or not collection_name:
            return client
            
        # Obtener colección específica
        db = client[db_name or settings.MONGO_DB_NAME]
        collection = db[collection_name]
        
        # Crear índices si es necesario (ejemplo)
        if collection_name == "medicationRequest":
            collection.create_index([("identifier.system", 1), ("identifier.value", 1)])
        
        return collection
        
    except ConnectionFailure as e:
        logging.error(f"Error de conexión a MongoDB: {str(e)}")
        raise ConnectionFailure(f"No se pudo conectar a MongoDB: {str(e)}")
    except ConfigurationError as e:
        logging.error(f"Configuración incorrecta: {str(e)}")
        raise ConfigurationError(f"Error en la configuración de MongoDB: {str(e)}")
    except Exception as e:
        logging.critical(f"Error inesperado: {str(e)}")
        raise Exception(f"Error desconocido al conectar a MongoDB: {str(e)}")
