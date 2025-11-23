from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import whois
from datetime import datetime
import logging

app = FastAPI()

# CORS pour le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

class WhoisRequest(BaseModel):
    domain: str

class WhoisResult(BaseModel):
    domain: str
    registrar: Optional[str] = None
    whois_server: Optional[str] = None
    creation_date: Optional[Any] = None
    expiration_date: Optional[Any] = None
    updated_date: Optional[Any] = None
    status: Optional[Any] = None
    name_servers: Optional[Any] = None
    emails: Optional[Any] = None

@app.post("/api/whois", response_model=WhoisResult)
def whois_lookup(request: WhoisRequest):
    try:
        data = whois.whois(request.domain)
        result = WhoisResult(
            domain=request.domain,
            registrar=data.get('registrar'),
            whois_server=data.get('whois_server'),
            creation_date=data.get('creation_date'),
            expiration_date=data.get('expiration_date'),
            updated_date=data.get('updated_date'),
            status=data.get('status'),
            name_servers=data.get('name_servers'),
            emails=data.get('emails')
        )
        return result
    except Exception as e:
        logging.error(f"Erreur WHOIS: {e}")
        raise HTTPException(status_code=400, detail=f"Erreur WHOIS: {e}")

@app.get("/api/health")
def health():
    return {"status": "ok"}
