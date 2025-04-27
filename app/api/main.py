from fastapi import FastAPI
from app.api import routes

####### ── Imports ────────────────────────────────────────────────────────
import time
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import router       # existing routes (chat, upload, etc.)
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for Chatbot, Uploading, Monitoring",
    version="1.0.0",
)

# Include API routes
app.include_router(routes.router)

Instrumentator().instrument(app).expose(app)
# Health check endpoint
@app.get("/")
def health():
    return {"status": "ok"}

#################
# ── Prometheus metrics ─────────────────────────────────────────────
HTTP_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)
HTTP_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency (seconds) per endpoint",
    ["method", "path"]
)

# ── FastAPI app ────────────────────────────────────────────────────
app = FastAPI(title="RAG Chatbot API", version="2.0.0")

# If you already have CORS settings, keep them; else minimal:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentation middleware
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    HTTP_COUNTER.labels(
        request.method,
        request.url.path,
        response.status_code
    ).inc()

    HTTP_LATENCY.labels(
        request.method,
        request.url.path
    ).observe(latency)

    return response

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Existing API endpoints
app.include_router(router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

