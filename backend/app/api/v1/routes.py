from fastapi import APIRouter


router = APIRouter()


@router.get("/health", summary="Public API health check")
async def health() -> dict[str, str]:
    """Simple public API health check endpoint."""
    return {"status": "ok"}

