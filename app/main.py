from typing import Any
from fastapi import FastAPI, HTTPException, Request
import logging 
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.v1 import api_router 
from app.utils.scheduler import SchedulerService
from app.config.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sch_srv: Any = None
settings: Settings = Settings()
#user.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
    

app.include_router(api_router, prefix='/api/v1')

# @app.exception_handler(HTTPException)
# def http_exception_handler(request: Request, exc: HTTPException):
#     logger.info(f"Request: {request.url.path} - {exc}")

#     return JSONResponse(
#         status_code=exc.status_code,
#         content=jsonable_encoder(
#             {
#                 "msg": f"An error occurred! {exc.detail}",
#                 "code": f"{exc.status_code}",
#                 "success": False,
#             }
#         ),
#     )
@app.on_event("startup")
async def run_scheduler():
    global sch_srv
    sch_srv = SchedulerService()
    sch_srv.start()

@app.on_event("shutdown")
async def pickle_schedule():
    sch_srv.stop()