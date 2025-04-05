from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.MedicationCrud import (
    GetMedicationRequestById,
    WriteMedicationRequest,
    GetMedicationRequestByIdentifier,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-medication-request.onrender.com"],
    allow_credetials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.get("/medicationRequest/{request_id}", response_model=dict)
async def get_request_by_id(request_id: str):
    status, request = GetMedicationRequestById(request_id)
    if status == 'success':
        return request
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="MedicationRequest not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/medicationRequest", response_model=dict)
async def get_request_by_identifier(system: str, value:str):
    status, request =GetMedicationRequestByIdentifier(system, value)
    if status == 'success':
        return request
    elif status == 'notFound':
        raise HTTPException(status_code=204, detail="MedicationRequest not found")
    else: 
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.post("/medicationRequest", response_model=dict)
async def add_request(request: Request):
    new_request_dict = dict(await request.json())
    status, request_id = WriteMedicationRequest(new_request_dict)
    if status == 'success':
        return {"_id": request_id}
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
