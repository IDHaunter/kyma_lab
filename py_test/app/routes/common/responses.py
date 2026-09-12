import html
import logging
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response, PlainTextResponse

logger = logging.getLogger(__name__)

class ErrorItem(BaseModel):
    message: str
    domain: str
    reason: str


class ErrorBlock(BaseModel):
    code: int
    title: str
    status: str
    errors: List[ErrorItem]
    debug: Optional[str] = None  # If debug_mode activated


class ErrorResponse(BaseModel):
    status: str = "error"
    error: ErrorBlock


class SuccessResponse(BaseModel):
    status: str = "success"
    code: int
    message: str
    data: Optional[Any] = None

class ResponseMessages:
    # Basic messages
    _ERROR_400 = {"code": 400, "title": "Bad request"}
    _ERROR_401 = {"code": 401, "title": "Unauthorized"}
    _ERROR_403 = {"code": 403, "title": "Forbidden"}
    _ERROR_404 = {"code": 404, "title": "Not found"}
    _ERROR_500 = {"code": 500, "title": "Internal server error"}

    _debug = True
    _default_format = 'json'  # may be 'text' or 'json'

    @classmethod
    def set_debug(cls, value: bool):
        cls._debug = value

    @classmethod
    def set_default_format(cls, format_type: str):
        """Set default response format ('text' or 'json')"""
        if format_type.lower() in ('text', 'json'):
            cls._default_format = format_type.lower()
        else:
            raise ValueError("Format must be either 'text' or 'json'")

    @staticmethod
    def _get_google_status(code: int) -> str:
        """Maps HTTP code to Google error status string."""
        return {
            400: "INVALID_ARGUMENT",
            401: "UNAUTHENTICATED",
            403: "PERMISSION_DENIED",
            404: "NOT_FOUND",
            500: "INTERNAL",
        }.get(code, "UNKNOWN")

    @staticmethod
    def _build_error_payload(
            error_data: Dict[str, Any],
            details: str = '',
            debug_details: str = ''
    ) -> Dict[str, Any]:
        message = html.escape(details) if details else error_data["title"]
        payload = {
            "status": "error",
            "error": {
                "code": error_data["code"],
                "title": error_data["title"],
                "errors": [
                    {
                        "message": message,
                        "domain": "global",
                        "reason": "invalid"
                    }
                ],
                "status": ResponseMessages._get_google_status(error_data["code"])
            }
        }

        if ResponseMessages._debug and debug_details:
            payload["error"]["debug"] = html.escape(debug_details)

        return payload

    @staticmethod
    def _create_error_response(
            error_data: Dict[str, Any],
            details: str = '',
            debug_details: str = '',
            response_format: str = None
    ) -> Response:
        fmt = response_format or ResponseMessages._default_format

        # Logging
        log_msg = f"Error {error_data['code']}: {error_data['title']} - {details}"
        if error_data["code"] == 404:
            logger.warning(log_msg)
        else:
            logger.error(log_msg)

        if fmt == 'json':
            # JSON format
            payload = ResponseMessages._build_error_payload(
                error_data, details, debug_details)

            return JSONResponse(
                content=payload,
                status_code=error_data["code"]
            )
        else:
            # Text format
            message = f"{error_data['title']}: {html.escape(details)}".strip()
            if ResponseMessages._debug and debug_details:
                message += f" (Debug: {html.escape(debug_details)})"

            return PlainTextResponse(
                content=message,
                status_code=error_data["code"]
            )

    @staticmethod
    def error_400(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages._ERROR_400, details, debug_details, response_format)

    @staticmethod
    def error_401(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages._ERROR_401, details, debug_details, response_format)

    @staticmethod
    def error_403(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages._ERROR_403, details, debug_details, response_format)

    @staticmethod
    def error_404(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages._ERROR_404, details, debug_details, response_format)

    @staticmethod
    def error_500(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages._ERROR_500, details, debug_details, response_format)

    # Success methods
    @staticmethod
    def success(message: str = '', data: dict = None, status_code: int = 200) -> JSONResponse:
        # Validate status code
        if not 200 <= status_code <= 299:
            raise ValueError(f"Invalid success status code: {status_code}. Must be in 200-299 range")

        # Log successful response
        logger.info(f"Success {status_code}: {message}")

        # Build response payload
        payload = {
            "status": "success",
            "code": status_code,
            "message": message
        }
        if data is not None:
            payload["data"] = data

        return JSONResponse(
            content=payload,
            status_code=status_code
        )

    # FastAPI-specific convenience methods
    @staticmethod
    def http_exception(
            status_code: int = 400,
            detail: str = '',
            debug_detail: str = ''
    ) -> HTTPException:
        """Create a FastAPI HTTPException with consistent error format"""
        error_mapping = {
            400: ResponseMessages._ERROR_400,
            401: ResponseMessages._ERROR_401,
            403: ResponseMessages._ERROR_403,
            404: ResponseMessages._ERROR_404,
            500: ResponseMessages._ERROR_500
        }

        error_data = error_mapping.get(status_code, ResponseMessages._ERROR_400)

        # Log the error
        log_msg = f"Error {status_code}: {error_data['title']} - {detail}"
        if status_code == 404:
            logger.warning(log_msg)
        else:
            logger.error(log_msg)

        # Build detailed error message
        message = detail or error_data["title"]
        if ResponseMessages._debug and debug_detail:
            message += f" (Debug: {debug_detail})"

        return HTTPException(
            status_code=status_code,
            detail=message
        )