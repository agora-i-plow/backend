from time import ctime, perf_counter

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.controllers.admin import admin_router
from app.controllers.customer import customer_router
from app.controllers.preview import preview_router
from app.controllers.producer import producer_router
from app.controllers.users import users_router
from app.services.mongo import Mongo
from app.services.postgres import Postgres
from app.utils.exceptions import CommonException, InternalServerError
from app.utils.logger import Log
from app.utils.matching import reformat_references

app = FastAPI(title="Reference matcher")


@app.on_event("startup")
async def startup() -> None:
    await Log.initialise_logger()
    await Postgres.connect_db()
    Mongo.connect_db()
    await reformat_references()


@app.on_event("shutdown")
async def shutdown() -> None:
    Mongo.disconnect_db()
    await Postgres.disconnect_db()
    await Log.shutdown_logger()


@app.exception_handler(CommonException)
async def common_exception_handler(request: Request, exception: CommonException):
    await Log.log_exception(exception)
    return JSONResponse(
        status_code=exception.code,
        content={"code": exception.code, "message": exception.message},
    )


@app.exception_handler(Exception)
async def unknown_exception(request: Request, exception: Exception):
    raise InternalServerError(exception) from exception


@app.middleware("http")
async def log_requst(request: Request, call_next):
    await Log.log_request_start(
        request.method, request.url.path, ctime(), request.client.host
    )
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    formatted_process_time = "{0:.5f}".format(process_time)
    await Log.log_request_end(
        request.method,
        request.url.path,
        ctime(),
        formatted_process_time,
        request.client.host,
    )
    return response


app.include_router(users_router)
app.include_router(admin_router)
app.include_router(producer_router)
app.include_router(customer_router)
app.include_router(preview_router)
