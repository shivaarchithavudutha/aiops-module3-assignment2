from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import redis

app = FastAPI(title="Spam Classifier API with Redis Cache")

class PredictRequest(BaseModel):
    text: str

model = None
redis_client = None

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 300))

@app.on_event("startup")
def startup():
    global model, redis_client
    model_path = os.getenv("MODEL_PATH", "model.joblib")
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        raise RuntimeError(f"Model file not found at {model_path}")
    
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_connect_timeout=2
        )
        redis_client.ping()
        print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        print(f"Redis unavailable ({e}). Fallback to uncached predictions.")
        redis_client = None

@app.get("/healthz")
def healthz():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "version": "v2"}

@app.post("/predict")
def predict(request: PredictRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Empty text supplied")
    
    cache_key = f"spam_pred:{request.text}"
    
    # 1. Cache HIT Check
    if redis_client:
        try:
            cached_label = redis_client.get(cache_key)
            if cached_label:
                return {"label": cached_label, "source": "cache"}
        except Exception:
            pass

    # 2. Cache MISS: Run model prediction
    prediction = model.predict([request.text])[0]

    # 3. Store result in Redis with TTL
    if redis_client:
        try:
            redis_client.setex(cache_key, CACHE_TTL_SECONDS, prediction)
        except Exception:
            pass

    return {"label": prediction, "source": "model"}
