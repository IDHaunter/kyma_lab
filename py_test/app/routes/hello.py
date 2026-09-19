from fastapi import APIRouter, Request, HTTPException

from app.routes.common.responses import SuccessResponse, COMMON_ERROR_RESPONSES
import logging
import json
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hello", tags=["hello"])

class HelloRequest(BaseModel):
    user_prefix: str
    user_name: str

@router.post(
    "/say",
    summary="Say Hello",
    description="Get user name and user prefix and say hello to them.",
    response_model=SuccessResponse,
    responses=COMMON_ERROR_RESPONSES
)
async def say_hello(
    payload: HelloRequest,
    request: Request
):
    func_name = 'say_hello'

    user = await _get_user_from_request(request)

    logger.info(
        f"{func_name}: user={user.get("id",'')}, payload={ json.dumps(payload.model_dump()) }"
    )

    # Empty input processing
    if not payload.user_name or not payload.user_name.strip():
        raise HTTPException(status_code=400, detail="User name is required.", )

    if len(payload.user_prefix)==1:
        raise HTTPException(status_code=400, detail="User prefix cannot be 1 character.", )

    message = "Hello "

    if payload.user_prefix:
        message = message + payload.user_prefix

    message = message + payload.user_name

    aa = 100/0

    return SuccessResponse(
        message = "Greetings",
        data={
            "message_id": 1,
            "message": message
        }
    )

# -------------------------------------- Helper Functions ------------------------------------------

async def _get_user_from_request(request: Request) -> dict:
    user = getattr(request.state, "user", {})

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. No user in request.")

    if not user.get("id"):
        raise HTTPException(status_code=401, detail="Unauthorized: no user id")

    # Create runtime copy and Add authorization header for runtime usage (webhooks, downstream calls)
    user = {
        **user,
        "user_token": request.headers.get("Authorization")
    }

    return user