import json
from pathlib import Path

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import ROOT, settings

app = FastAPI(title="StarBook API")


# Check if storage JSON file exists and create if not
@app.on_event("startup")
def check_storage_file():
    storage_file = Path(ROOT / settings.STORAGE_FILE_NAME)
    if not storage_file.exists():
        storage_file.touch()
        initial_data = {"stars": [], "constellations": []}
        with open(storage_file, 'w') as f:
            json.dump(initial_data, f)


app.include_router(api_router, prefix=settings.API_PATH)
