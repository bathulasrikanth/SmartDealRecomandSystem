# deals/utils.py
import os
import joblib
from django.conf import settings

MODEL_PATHS = [
    os.path.join(settings.BASE_DIR, "deals", "ml", "model.pkl"),
    os.path.join(settings.BASE_DIR, "saved_models", "model.pkl"),
    os.path.join(settings.BASE_DIR, "model.pkl"),
]

META_PATHS = [
    os.path.join(settings.BASE_DIR, "deals", "ml", "model_metadata.pkl"),
    os.path.join(settings.BASE_DIR, "saved_models", "model_metadata.pkl"),
    os.path.join(settings.BASE_DIR, "model_metadata.pkl"),
]

_model = None
_metadata = None

def get_model():
    global _model
    if _model is None:
        for p in MODEL_PATHS:
            if os.path.exists(p):
                _model = joblib.load(p)
                print(f"[get_model] Loaded model from: {p}")
                break
        else:
            raise FileNotFoundError("model.pkl not found. Searched:\n" + "\n".join(MODEL_PATHS))
    return _model

def get_metadata():
    global _metadata
    if _metadata is None:
        for p in META_PATHS:
            if os.path.exists(p):
                _metadata = joblib.load(p)
                print(f"[get_metadata] Loaded metadata from: {p}")
                break
        else:
            # If metadata not found, try to infer basic columns from the pipeline if possible
            print("[get_metadata] metadata file not found; returning None")
            _metadata = None
    return _metadata
