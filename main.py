import os
import uvicorn

from fastapi import FastAPI,Request
from utils.routes import router as api_router
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException  

# Load the environment variables from .env file
load_dotenv()

app = FastAPI(debug=True)

# Include the router from the routes file
app.include_router(api_router)

# Custom exception handler for RequestValidationError (validation errors)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = f"{field} is required"
        error_messages.append({"message": msg,"code":'OTZ422'})   
    return JSONResponse(status_code=422, content={"status": False, "errors": error_messages})

@app.exception_handler(StarletteHTTPException)
async def authentication_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status": False, "errors": [{"message":"Please provide valid authorization token","code":'OTZ401',"reason": exc.detail}]})


allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)


if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get("HOST"), port=os.environ.get("PORT"))
