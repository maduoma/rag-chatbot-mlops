from fastapi import APIRouter

from app.api.routes.chat_routes import router as chat_router
from app.api.routes.upload_routes import router as upload_router
from app.api.routes.metrics_routes import router as metrics_router
from app.api.routes.health_routes import router as health_router
from app.api.routes.admin_routes import router as admin_router  # Optional

router = APIRouter()

# Grouped Routes
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(metrics_router, prefix="/metrics", tags=["Monitoring"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])  # Optional
