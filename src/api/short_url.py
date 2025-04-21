from fastapi import APIRouter

short_url_router = APIRouter()

@short_url_router.get("/")
async def root():
    return {"message": "short_url_router"}
