import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Función para conectar a la base de datos MongoDB
def connect_to_mongodb(uri, db_name, collection_name):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection

# Función para guardar un recurso MedicationRequest en MongoDB
def save_medication_request_to_mongodb(med_request_json, collection):
    try:
        # Convertir el JSON string a un diccionario de Python
        med_data = json.loads(med_request_json)

        # Insertar el documento en la colección de MongoDB
        result = collection.insert_one(med_data)

        # Retornar el ID del documento insertado
        return result.inserted_id
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Cadena de conexión a MongoDB
    uri = "mongodb+srv://21vanessaaa:VANEifmer2025@sampleinformationservic.ceivw.mongodb.net/?retryWrites=true&w=majority&appName=SampleInformationService"
    # Nombre de la base de datos y la colección
    db_name = "EntregaDeMedicamentos"
    collection_name = "MedicationRequest" 

    # Conectar a MongoDB
    collection = connect_to_mongodb(uri, db_name, collection_name)

    # JSON de ejemplo para MedicationRequest
    med_request_json = '''
    {
      "resourceType": "MedicationRequest",
      "id": "medrx001",
      "status": "active",
      "intent": "order",
      "medicationCodeableConcept": {
        "coding": [
          {
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
            "code": "1049502",
            "display": "Amoxicillin 250mg/5ml Suspension"
          }
        ],
        "text": "Amoxicillin 250mg/5ml Suspension"
      },
      "subject": {
        "reference": "Patient/1020713756",
        "display": "Mario Enrique Duarte"
      },
      "authoredOn": "2024-04-01",
      "requester": {
        "reference": "Practitioner/12345",
        "display": "Dr. Carolina Torres"
      },
      "dosageInstruction": [
        {
          "text": "Tomar 5 ml cada 8 horas durante 7 días"
        }
      ],
      "dispenseRequest": {
        "quantity": {
          "value": 1,
          "unit": "frasco"
        }
      }
    }
    '''

    # Guardar el recurso MedicationRequest en MongoDB
    inserted_id = save_medication_request_to_mongodb(med_request_json, collection)

    if inserted_id:
        print(f"Entrega de medicamento guardada con ID: {inserted_id}")
    else:
        print("No se pudo guardar la entrega de medicamento.")
        
