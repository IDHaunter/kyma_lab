import logging
from pydantic import BaseModel
from typing import Any, Optional

logger = logging.getLogger(__name__)

class SuccessResponse(BaseModel):
    status: str = "success"
    code: int = 200
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    detail: str

COMMON_ERROR_RESPONSES = {
    400: {
        "model": ErrorResponse,
        "description": "Bad request. The request parameters are invalid."
    },
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized. Authentication is required."
    },
    403: {
        "model": ErrorResponse,
        "description": "Forbidden. The authenticated user is not allowed to perform this operation."
    },
    404: {
        "model": ErrorResponse,
        "description": "Not found. The requested resource does not exist."
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal server error. An unexpected error occurred while processing the request."
    },
}