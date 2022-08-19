from time import perf_counter, ctime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils.logger import Log
from app.services.postgres import Postgres
from app.utils.exceptions import CommonException, InternalServerError

from app.controllers.users import users_router

app = FastAPI(title='Reference matcher')

@app.on_event('startup')
async def startup() -> None:
    await Log.initialise_logger()
    await Postgres.connect_db()

@app.on_event('shutdown')
async def shutdown() -> None:
    await Postgres.disconnect_db()
    await Log.shutdown_logger()

@app.exception_handler(CommonException)
async def common_exception_handler(request: Request, exception: CommonException):
    await Log.log_exception(exception)
    return JSONResponse(
        status_code=exception.code,
        content={
            'code': exception.code,
            'message': exception.message
        }
    )

@app.exception_handler(Exception)
async def unknown_exception(request: Request, exception: Exception):
    raise InternalServerError(exception) from exception

@app.middleware("http")
async def log_requst(request: Request, call_next):
    await Log.log_request_start(request.method,request.url.path,ctime(),request.client.host)
    start_time = perf_counter()
    response = await call_next(request)
    process_time = (perf_counter() - start_time)
    formatted_process_time = '{0:.5f}'.format(process_time)
    await Log.log_request_end(request.method,request.url.path,ctime(),formatted_process_time,request.client.host)
    return response

app.include_router(users_router)