from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Statistics"]
)

@router.get("/test")
async def test():
    return {"message": "API работает"}
