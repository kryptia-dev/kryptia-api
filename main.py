import os, json
from typing import Optional

from fastapi import FastAPI, Query, Depends, HTTPException

from database      import init_db, get_session
from models        import Patch, Severity
from auth          import require_api_key


app = FastAPI()

# Ensure our SQLite tables exist
init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Kryptia API"}
...


@app.get("/status")
def status():
    return {
        "status": "running",
        "version": "0.1"
    }


@app.get("/patches/{patch_id}")
def get_patch(patch_id: int):
    patches = [
        {"id": 1, "name": "Patch Tuesday - June 2025", "severity": "High", "product": "Windows 11"},
        {"id": 2, "name": "Zero-Day Hotfix KB501", "severity": "Critical", "product": "Windows 10"},
        {"id": 3, "name": "Update Rollup KB600", "severity": "Medium", "product": "Windows Server"}
    ]

    for patch in patches:
        if patch["id"] == patch_id:
            return patch
    return {"error": f"Patch with id {patch_id} not found."}

from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Existing routes...

# Define patch schema for input
class Patch(BaseModel):
    id: int
    name: str
    severity: str
    product: str

patches = [
    {"id": 1, "name": "Patch Tuesday - June 2025", "severity": "High", "product": "Windows 11"},
    {"id": 2, "name": "Zero-Day Hotfix KB501", "severity": "Critical", "product": "Windows 10"},
    {"id": 3, "name": "Update Rollup KB600", "severity": "Medium", "product": "Windows Server"},
]

@app.post("/patches", response_model=Patch)
def create_patch(patch: Patch):
    patches.append(patch.dict())
    return patch

from typing import Optional, List
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

# Pydantic Model
class Patch(BaseModel):
    id: int
    name: str
    severity: str
    product: str

# Simulated in-memory database
patches_db: List[Patch] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Kryptia API"}

@app.get("/status")
def status():
    return {"status": "running", "version": "0.1"}

@app.post("/patches")
def create_patch(patch: Patch):
    patches_db.append(patch)
    return {"message": "Patch added", "patch": patch}

from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Patch(BaseModel):
    id: int
    name: str
    severity: str
    product: str

patches = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Kryptia API"}

@app.get("/status")
def status():
    return {"status": "running", "version": "0.1"}

@app.post("/patches")
def create_patch(patch: Patch):
    for existing in patches:
        if existing["id"] == patch.id:
            raise HTTPException(status_code=400, detail="Patch with this ID already exists")
    patches.append(patch.dict())
    return patch

import json
import os
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

PATCHES_FILE = "patches.json"

class Patch(BaseModel):
    id: int
    name: str
    severity: str
    product: str

# Load existing patches (or start with empty list)
if os.path.exists(PATCHES_FILE):
    with open(PATCHES_FILE, "r") as f:
        patches = json.load(f)
else:
    patches = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Kryptia API"}

@app.get("/status")
def status():
    return {"status": "running", "version": "0.1"}

@app.post("/patches")
def create_patch(patch: Patch):
    for existing in patches:
        if existing["id"] == patch.id:
            raise HTTPException(status_code=400, detail="Patch with this ID already exists")
    patch_dict = patch.dict()
    patches.append(patch_dict)

    # Save to JSON file
    with open(PATCHES_FILE, "w") as f:
        json.dump(patches, f, indent=4)

    return patch_dict

import json
import os

@app.post("/patches")
def create_patch(patch: Patch):
    # Load existing patches if file exists
    patches = []
    if os.path.exists("patches.json"):
        with open("patches.json", "r") as f:
            patches = json.load(f)
    
    # Check for duplicate ID
    if any(p["id"] == patch.id for p in patches):
        return {"detail": "Patch with this ID already exists"}, 422

    # Add new patch
    patches.append(patch.dict())

    # Save back to file
    with open("patches.json", "w") as f:
        json.dump(patches, f, indent=2)

    return patch

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI()

class Patch(BaseModel):
    id: int
    name: str
    severity: str
    product: str

@app.get(
    "/patches",
    response_model=list[Patch],
    summary="Get all patches (requires API key)"
)
def get_patches(
    severity: Optional[str] = Query(None),
    product:  Optional[str] = Query(None),
    _key:     None       = Depends(require_api_key),  # ← enforces your API-Key
):
    patches = []
    if os.path.exists("patches.json"):
        with open("patches.json", "r") as f:
            patches = json.load(f)

    if severity:
        patches = [p for p in patches if p["severity"].lower() == severity.lower()]
    if product:
        patches = [p for p in patches if p["product"].lower()  == product.lower()]

    return patches

@app.post("/patches")
def create_patch(patch: Patch):
    patches = []
    if os.path.exists("patches.json"):
        with open("patches.json", "r") as f:
            patches = json.load(f)

    if any(p["id"] == patch.id for p in patches):
        return {"detail": "Patch with this ID already exists"}, 422

    patches.append(patch.dict())

    with open("patches.json", "w") as f:
        json.dump(patches, f, indent=2)

    return patch

@app.patch("/patches/{patch_id}")
def update_patch(patch_id: int, updated_patch: Patch):
    patches = []

    if os.path.exists("patches.json"):
        with open("patches.json", "r") as f:
            patches = json.load(f)

    for index, patch in enumerate(patches):
        if patch["id"] == patch_id:
            patches[index] = updated_patch.dict()
            with open("patches.json", "w") as f:
                json.dump(patches, f, indent=2)
            return updated_patch

    return {"detail": "Patch not found"}, 404

@app.delete("/patches/{patch_id}")
def delete_patch(patch_id: int):
    if not os.path.exists("patches.json"):
        return {"detail": "No patches found"}, 404

    with open("patches.json", "r") as f:
        patches = json.load(f)

    updated_patches = [p for p in patches if p["id"] != patch_id]

    if len(updated_patches) == len(patches):
        return {"detail": "Patch not found"}, 404

    with open("patches.json", "w") as f:
        json.dump(updated_patches, f, indent=2)

    return {"message": f"Patch {patch_id} deleted"}



