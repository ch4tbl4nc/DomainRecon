# =============================================================================
# DomainRecon - Module de Scan
# =============================================================================

import socket
from typing import Optional
import httpx
import tldextract
import whois

# Headers de sécurité OWASP à vérifier
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
]


def extract_domain(url_or_domain: str) -> str:
    """Extrait le domaine d'une URL."""
    extracted = tldextract.extract(url_or_domain)
    return f"{extracted.domain}.{extracted.suffix}"


def resolve_ip(domain: str) -> Optional[str]:
    """Résout l'IP d'un domaine."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


async def check_security_headers(domain: str) -> dict:
    """Analyse les headers de sécurité HTTP."""
    result = {"headers_found": {}, "headers_missing": [], "score": "0/7", "error": None}
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, verify=False) as client:
        for url in [f"https://{domain}", f"http://{domain}"]:
            try:
                response = await client.head(url)
                for header in SECURITY_HEADERS:
                    value = response.headers.get(header)
                    if value:
                        result["headers_found"][header] = value
                    else:
                        result["headers_missing"].append(header)
                result["score"] = f"{len(result['headers_found'])}/{len(SECURITY_HEADERS)}"
                return result
            except Exception as e:
                result["error"] = str(e)
    
    result["headers_missing"] = SECURITY_HEADERS.copy()
    return result


def get_whois_data(domain: str) -> dict:
    """Récupère les informations WHOIS d'un domaine."""
    try:
        w = whois.whois(domain)
        
        # Gestion des dates (peut être liste ou valeur unique)
        def format_date(date_val):
            if isinstance(date_val, list):
                return str(date_val[0]) if date_val else None
            return str(date_val) if date_val else None
        
        return {
            "registrar": w.registrar,
            "creation_date": format_date(w.creation_date),
            "expiration_date": format_date(w.expiration_date),
            "name_servers": w.name_servers if isinstance(w.name_servers, list) else [w.name_servers] if w.name_servers else [],
            "status": w.status[0] if isinstance(w.status, list) else w.status,
            "raw": None
        }
    except Exception as e:
        return {
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "name_servers": [],
            "status": "error",
            "raw": str(e)
        }


async def perform_full_scan(url_or_domain: str) -> dict:
    """Effectue un scan complet d'un domaine."""
    domain = extract_domain(url_or_domain)
    
    # 1. Résolution DNS
    ip_address = resolve_ip(domain)
    
    # 2. Analyse des headers de sécurité (async)
    security_headers = await check_security_headers(domain)
    
    # 3. Récupération WHOIS (placeholder)
    whois_data = get_whois_data(domain)
    
    # Détermination du statut global
    status = "success"
    error_message = None
    
    if ip_address is None:
        status = "partial"
        error_message = "Impossible de résoudre l'adresse IP du domaine"
    
    if security_headers.get("error") and ip_address is None:
        status = "error"
        error_message = f"Scan échoué: {security_headers.get('error')}"
    
    return {
        "domain": domain,
        "ip_address": ip_address,
        "security_headers": security_headers,
        "whois_data": whois_data,
        "status": status,
        "error_message": error_message
    }
