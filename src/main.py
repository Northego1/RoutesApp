import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.v1 import router
from container import Container
from core import schema
from core.middlewares.protected_middleware import ProtectedMiddleware


def create_container() -> Container:
    return Container()


def create_app() -> FastAPI:
    app = FastAPI(
        responses={
            422: {"model": schema.ApiResponse[None, schema.ValidationResponseDetails]},
        },
    )
    app.include_router(router)

    app.add_middleware(ProtectedMiddleware)
    app.state.container = create_container()
    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=schema.ApiResponse(
            status=schema.Status.FAILURE,
            detail=exc.errors(),
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def auth_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=schema.ApiResponse(
            status=schema.Status.FAILURE,
            detail=exc.detail,
        ).model_dump(),
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
