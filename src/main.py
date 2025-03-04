import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from api.v1 import router
from container import Container
from core import schema


def create_container() -> Container:
    return Container()


def create_app() -> FastAPI:
    app = FastAPI(
        responses={
            422: {"model": schema.ApiResponse[None, schema.ValidationResponseDetails]},
        },
    )
    app.include_router(router)
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
        ),
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
