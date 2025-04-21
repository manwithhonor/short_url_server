from fastapi import APIRouter, status, HTTPException
from src.api.short_url import short_url_router
from src.api.user import user_router
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

base_router = APIRouter()
base_router.include_router(short_url_router, prefix="/short_url", tags=["short_url"])
base_router.include_router(user_router, prefix="/users", tags=["users"])

@base_router.delete("/")
async def root():
    return {"message": "Hello World"}

@base_router.post("/hello/{name}",
                  summary="test summary",
                  response_description="A greeting for the person")
async def say_hello(name: str):
    """Test documentation"""
    return {"message": f"Hello {name}"}

@base_router.post("/inc{number}")
async def increment(number: int):
    """Test documentation"""
    if number < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number must be positive")
    return {"message": number + 1}

@base_router.post("/test_func",
                  status_code=status.HTTP_202_ACCEPTED,
                  response_class=HTMLResponse)
async def test_func():
    return "<h1>test</h1>"
    # return  "test message"


# @app.get('/filter')
# async def filter_handler(param1, param2):
#     return {
#         'action': 'filter',
#         'param1': param1,
#         'param2': param2
#     }
