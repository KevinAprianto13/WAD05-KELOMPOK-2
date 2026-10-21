import sys
import os
from pathlib import Path

# Tambahkan direktori backend ke sys.path agar modul 'app' dapat diimport
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import instance FastAPI app
from app.main import app
