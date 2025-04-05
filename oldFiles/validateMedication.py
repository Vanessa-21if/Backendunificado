from fhir.resources.medicationrequest import MedicationRequest
import json

# Ejemplo de uso
if __name__ == "__main__":
    # JSON string correspondiente al artefacto MedicationRequest de HL7 FHIR
    medication_request_json = '''
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

    # Validar y parsear el JSON como un recurso MedicationRequest
    med_request = MedicationRequest.model_validate(json.loads(medication_request_json))

    # Mostrar el resultado como diccionario Python
    print("Entrega de Medicamento (JSON validado)::")
    print(json.dumps(med_request.model_dump(), indent=2, ensure_ascii=False))
    
