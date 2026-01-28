from fastapi import APIRouter


router = APIRouter()


@router.get("/healthz", summary="Internal health check")
async def healthz() -> dict[str, str]:
    """Simple internal health check endpoint."""
    return {"status": "ok"}

