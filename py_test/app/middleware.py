import base64
import binascii
import logging
import secrets

from fastapi import Request
from app.routes.common.responses import ResponseMessages
from app.settings import DEBUG

logger = logging.getLogger(__name__)

if not logging.getLogger().hasHandlers():
    print(f"ERROR: Root logger had no handlers. Logging unavailable in module {__name__}.")

PUBLIC_ENDPOINTS = {'/', '/docs', '/openapi.json', '/favicon.ico', '/static/logo.png'}
ADMIN_ENDPOINTS = {'/logs'}


async def check_authorization(request: Request, call_next):
    try:
        # Public endpoints
        if request.url.path in PUBLIC_ENDPOINTS:
            logger.info(f'----> "{request.url.path}" is public')
            return await call_next(request)

        payload = {}

        if DEBUG:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Basic "):
                return ResponseMessages.error_401("Missing or invalid Authorization header")

            credentials = auth_header[len("Basic "):].strip()

            try:
                # Decode base64 bytes and convert to string
                decoded_credentials = base64.b64decode(credentials).decode("utf-8")

                # Split into username and password
                user_name, password = decoded_credentials.split(":", 1)

                # Validate admin
                if user_name == "admin" and secrets.compare_digest(password, "admin"):
                    payload = {"sub": user_name, "is_admin": True, "is_reader": True}
                
                # Validate reader
                elif user_name == "reader" and secrets.compare_digest(password, "reader"):
                    payload = {"sub": user_name, "is_admin": False, "is_reader": True}
                
                else:
                    return ResponseMessages.error_401("Invalid username or password")

            except (ValueError, UnicodeDecodeError, binascii.Error):
                return ResponseMessages.error_401("Invalid Basic Auth credentials format")

        else:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return ResponseMessages.error_401("Missing or invalid Authorization header")

            token = auth_header[len("Bearer "):].strip()

            if not token:
                return ResponseMessages.error_401("Missing access token")
            
            # TODO: Replace temporary payload with actual JWT verification logic
            payload = {"sub": "user123", "is_admin": True, "is_reader": True}

        # Place the user state on the request
        request.state.user = {
            "id": payload["sub"],
            "is_admin": payload.get("is_admin", False),
            "is_reader": payload.get("is_reader", False),
        }

        # Check admin access
        if request.url.path in ADMIN_ENDPOINTS:
            if not request.state.user["is_admin"]:
                return ResponseMessages.error_403("Admin access only")

        logger.info(f'Authorization passed for "{request.url.path}"')
        return await call_next(request)

    except Exception as e:
        logger.exception("Middleware execution failed")
        return ResponseMessages.error_500(f"Middleware error on path {request.url.path}: {str(e)}")