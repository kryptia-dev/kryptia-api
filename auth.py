# auth.py
from fastapi import Header, HTTPException

# 🔑 change this to something truly secret!
API_KEY    = "your-super-secret-key"
API_HEADER = "x-api-key"

async def require_api_key(x_api_key: str = Header(..., alias=API_HEADER)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
