# =============================================================================
# DomainRecon - API FastAPI
# =============================================================================

from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import engine, get_db, Base
from .models import Scan
from .scanner import perform_full_scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crée les tables au démarrage."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DomainRecon API",
    description="API OSINT pour la reconnaissance de domaines",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Schémas Pydantic
# =============================================================================

class ScanRequest(BaseModel):
    domain: str = Field(..., min_length=3, max_length=255)


class SecurityHeadersResponse(BaseModel):
    headers_found: dict = Field(default_factory=dict)
    headers_missing: list = Field(default_factory=list)
    score: str = "0/7"
    error: Optional[str] = None


class WhoisDataResponse(BaseModel):
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    name_servers: list = Field(default_factory=list)
    status: Optional[str] = None
    raw: Optional[str] = None


class ScanResponse(BaseModel):
    id: int
    domain: str
    ip_address: Optional[str] = None
    security_headers: SecurityHeadersResponse
    whois_data: WhoisDataResponse
    scan_timestamp: datetime
    status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    total: int
    scans: list[ScanResponse]


# =============================================================================
# Routes
# =============================================================================

@app.get("/", tags=["Health"])
async def root():
    return {"status": "online", "message": "DomainRecon API", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"api": "healthy", "database": "connected"}
    except Exception as e:
        return {"api": "healthy", "database": f"error: {e}"}


@app.post("/scan", response_model=ScanResponse, tags=["Scan"])
async def scan_domain(request: ScanRequest, db: Session = Depends(get_db)):
    """Scan un domaine et sauvegarde le résultat."""
    try:
        result = await perform_full_scan(request.domain)
        
        db_scan = Scan(
            domain=result["domain"],
            ip_address=result["ip_address"],
            security_headers=result["security_headers"],
            whois_data=result["whois_data"],
            scan_timestamp=datetime.utcnow(),
            status=result["status"],
            error_message=result["error_message"]
        )
        
        db.add(db_scan)
        db.commit()
        db.refresh(db_scan)
        
        return ScanResponse(
            id=db_scan.id,
            domain=db_scan.domain,
            ip_address=db_scan.ip_address,
            security_headers=SecurityHeadersResponse(**db_scan.security_headers),
            whois_data=WhoisDataResponse(**db_scan.whois_data),
            scan_timestamp=db_scan.scan_timestamp,
            status=db_scan.status,
            error_message=db_scan.error_message
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=HistoryResponse, tags=["History"])
async def get_scan_history(
    limit: int = 10,
    offset: int = 0,
    domain: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupère l'historique des scans."""
    query = db.query(Scan)
    
    if domain:
        query = query.filter(Scan.domain.contains(domain))
    
    total = query.count()
    scans = query.order_by(Scan.scan_timestamp.desc()).offset(offset).limit(limit).all()
    
    return HistoryResponse(
        total=total,
        scans=[
            ScanResponse(
                id=s.id,
                domain=s.domain,
                ip_address=s.ip_address,
                security_headers=SecurityHeadersResponse(**(s.security_headers or {})),
                whois_data=WhoisDataResponse(**(s.whois_data or {})),
                scan_timestamp=s.scan_timestamp,
                status=s.status,
                error_message=s.error_message
            ) for s in scans
        ]
    )


@app.get("/scan/{scan_id}", response_model=ScanResponse, tags=["Scan"])
async def get_scan_by_id(scan_id: int, db: Session = Depends(get_db)):
    """Récupère un scan par son ID."""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan non trouvé")
    
    return ScanResponse(
        id=scan.id,
        domain=scan.domain,
        ip_address=scan.ip_address,
        security_headers=SecurityHeadersResponse(**(scan.security_headers or {})),
        whois_data=WhoisDataResponse(**(scan.whois_data or {})),
        scan_timestamp=scan.scan_timestamp,
        status=scan.status,
        error_message=scan.error_message
    )

