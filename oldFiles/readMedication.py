from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

def connect_to_mongodb(uri, db_name, collection_name):
    """Conectar a la base de datos MongoDB"""
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection

def read_medication_requests_from_mongodb(collection):
    """Leer todas las órdenes de medicación de la colección"""
    try:
        medication_requests = collection.find()
        return list(medication_requests)
    except Exception as e:
        print(f"Error al leer desde MongoDB: {e}")
        return None

def display_medication_requests(medication_list):
    """Mostrar los datos de las órdenes de medicación"""
    if medication_list:
        for med in medication_list:
            print("Orden de Medicación:")
            print(f"  ID: {med.get('_id')}")
            print(f"  Medicamento: {med.get('medicationCodeableConcept', {}).get('text', 'Desconocido')}")
            print(f"  Estado: {med.get('status', 'Desconocido')}")
            print(f"  Paciente: {med.get('subject', {}).get('display', 'Desconocido')}")
            print(f"  Médico: {med.get('requester', {}).get('display', 'Desconocido')}")
            print(f"  Fecha prescripción: {med.get('authoredOn', 'Desconocida')}")
            print(f"  Dosis: {med.get('dosageInstruction', [{}])[0].get('text', 'No especificada')}")
            print("-" * 50)
    else:
        print("No se encontraron órdenes de medicación en la base de datos.")

if __name__ == "__main__":
    # Configuración de conexión
    uri = "mongodb+srv://21vanessaaa:VANEifmer2025@sampleinformationservic.ceivw.mongodb.net/?retryWrites=true&w=majority&appName=SampleInformationService"
    db_name = "EntregaDeMedicamentos"
    collection_name = "MedicationRequest"

    # Conectar a MongoDB
    collection = connect_to_mongodb(uri, db_name, collection_name)
    
    # Leer las órdenes de medicación de la colección
    medication_requests = read_medication_requests_from_mongodb(collection)
    
    # Mostrar los datos de las órdenes de medicación
    display_medication_requests(medication_requests)
