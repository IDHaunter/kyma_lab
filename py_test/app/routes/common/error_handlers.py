from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.routes.common.responses import ResponseMessages


def register_error_handlers(app: FastAPI):
    # universal handler HTTPException
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == 400:
            return ResponseMessages.error_400(str(exc.detail))
        elif exc.status_code == 401:
            return ResponseMessages.error_401(str(exc.detail))
        elif exc.status_code == 403:
            return ResponseMessages.error_403(str(exc.detail))
        elif exc.status_code == 404:
            return ResponseMessages.error_404(str(exc.detail))
        elif exc.status_code == 500:
            return ResponseMessages.error_500(str(exc.detail))
        else:
            # for other errors we just return standard JSON
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": str(exc.detail)},
            )

    # fallback for unexpected errors (similar to 500)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return ResponseMessages.error_500(str(exc))
