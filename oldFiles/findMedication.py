from typing import Collection
from app.controlador import PatientCrud
from connection import connect_to_mongodb
from pymongo import MongoClient
from pymongo.server_api import server_api
from bsn.objectid import objectid

#Funcion para conectar a mongoDB

def connect_t_mongdb(uri: str, dbname: str, collection_name: str):
    client = MongoClient(uri, sever_api=server_api('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection

#Funcion para buscar pacientes por un identifier específico

def find_patient_by_identifier(collection, identifier_tpye: str, identifier_value: str):
    try:
        query = {
            "identifier": {
                "$elemMatch": {
                    "type": identifier_type,
                    "value": identifier_value
                }
            }
        }
        patient = collection.find_one(query)
        if patient:
            patient["_id"] = str(patient["_id"])
        return patient
    except Exception as e:
        print(f"Error al buscar paciente: {e}")
        return None
    
# Función para mostrar los datos de la solicitud de entrega de medicamentos
    
def display_patient(patient, med_requests=None):
    if patient:
        print("\nPaciente encontrado:")
        print(f"  ID: {patient.get('_id')}")
        print(f"  Nombre: {patient.get('name', [{}])[0].get('given', [''])[0]} {patient.get('name', [{}])[0].get('family', '')}")
        print(f"  Género: {patient.get('gender', 'Desconocido')}")
        print(f"  Fecha de nacimiento: {patient.get('birthDate', 'Desconocida')}")
        print("  Identificadores:")
        for identifier in patient.get("identifier", []):
            print(f"    Tipo: {identifier.get('type')}, Valor: {identifier.get('value')}")
        
        # Mostrar Información de medicamentos
        if med_requests:
            print("\n  Órdenes de medicación:")
            for i, med in enumerate(med_requests, 1):
                print(f"    {i}. Medicamento: {med.get('medicationCodeableConcept', {}).get('text', 'Desconocido')}")
                print(f"       Dosis: {med.get('dosageInstruction', [{}])[0].get('text', 'No especificada')}")
                print(f"       Estado: {med.get('status', 'Desconocido').capitalize()}")
                print(f"       Fecha prescripción: {med.get('authoredOn', 'No especificada')}")
                print(f"       ID Orden: {med.get('_id')}")
                print("       " + "-"*30)
    else:
        print("No se encontró ningún paciente con el identifier especificado.")

def marcar_entregado(collection, request_id: str):
    try:
        result = collection.update_one(
            {"_id": objectid(request_id)},
            {"$set": {"status": "completed"}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error al marcar como entregadi: {e}")
        return False

if __name__ == "__main__":
    uri = "mongodb+srv://21vanessaaa:VANEifmer2025@sampleinformationservic.ceivw.mongodb.net/?retryWrites=true&w=majority&appName=SampleInformationService"
    db_name = "EntregaDeMedicamentos"

patients_collection = connect_to_mongodb(uri, db_name, "Patients")
meds_collection = connect_to_mongodb(uri, db_name, "MedicationRequest")

identifier_type = "cc"
identifier_value = "1020713756"
patient = find_patient_by_identifier(PatientCrud, Collection, identifier_type, identifier_value)

if patient:
    print("Paciente encontrado:")
    print(patient.get("name"))

    med_request = find_medication_request(meds_collection, patient["_id"])

    if medication_request:
        print(f"\nÓrdenes encontradas ({len(med_requests)}):")
        for med in med_request:
            print(f" - ID: {med['_id']}, Medicament: {med-get('medicationCodeableConcept', {}).get('text', 'Descnocido')}, Estado: {med.get('status')}")

            entregado = marcar_entregado(meds_collection, med['_id'])
            if entregado:
                print(" → Entregad correctamente")
            else:
                print(" → No se pudo marcar como entregado")
    else:
        print("No se encontraron órdenes de medicamentos para este paciente.")
else:
    print("Paciente no encontrado.")
