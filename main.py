from fastapi import FastAPI
from src.api import base
# from fastapi.responses import ORJSONResponse

app = FastAPI(redoc_url="/redoc_test",
              docs_url="/docs",
              openapi_url='/openapi.json',
              # default_response_class=ORJSONResponse,
              version="1.0.0.25465",
              title="our first application",
              description="This is a sample FastAPI application.",
              contact={
                  "name": "John Doe",
                  "url": "https://github.com/JohnDoe",
                  "email": "john.doe@example.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              }
              )

app.include_router(base.base_router, prefix="/api")
