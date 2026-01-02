import qrcode
import io
import base64
import secrets
import string
import json
from typing import Tuple

def generate_unique_token(length: int = 32) -> str:
    """Generate a high-entropy random token"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_qr_code_image(data: str, size: int = 10, border: int = 4) -> str:
    """Generates the actual PNG bytes and encodes to Base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def generate_qr_code_for_office(
    office_id: int, 
    office_name: str, 
    office_public_ip: str = None
) -> Tuple[str, str, str]:
    """Orchestrates token generation and image creation"""
    qr_token = generate_unique_token()
    qr_data = {
        "token": qr_token,
        "office_id": office_id,
        "office_name": office_name,
        "public_ip": office_public_ip
    }
    
    qr_data_json = json.dumps(qr_data)
    qr_image = generate_qr_code_image(qr_data_json)
    
    return qr_token, qr_data_json, qr_image