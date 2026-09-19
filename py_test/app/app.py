import os
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.settings import (APP_MODE, APP_NAME, APP_VER, DEBUG, PORT, HOST, WORKERS)
from app.routes.common.responses import SuccessResponse
from app.routes.root import router as root_router
from app.routes.hello import router as hello_router
from app.middleware import check_authorization

logger = logging.getLogger(__name__)

if not logging.getLogger().hasHandlers():
    print(f"ERROR: Root logger had no handlers. Logging unavailable in module {__name__}.")

# Application startup logs
logger.info(f"------ START : {APP_NAME.upper()}")
logger.info(f"     version : {APP_VER['ver']}")
logger.info(f"        date : {APP_VER['date']}")
logger.info(f"        info : {APP_VER['info']}")

if APP_MODE == DEBUG:
    logger.info(f"Debug (local deployment): {DEBUG}")
    logger.info(f"Server port: {PORT}")
    logger.info(f"Server host: {HOST}")
    logger.info(f"Server workers: {WORKERS}")

# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VER["ver"],
    debug=DEBUG
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register routers
app.include_router(root_router)
app.include_router(hello_router)

# Register Options (preflight) Handler
@app.options("/{path:path}")
async def options_handler(path: str):
    return SuccessResponse(
        message="Greetings",
        data={}
    )

# Register middleware
@app.middleware("http")
async def authorization_middleware(request: Request, call_next):
    return await check_authorization(request, call_next)

logger.debug('------ ENDPOINTS :')
for r in app.routes:
    logger.debug(r.path)
logger.debug('------')

# Application entry point (will work in local deployment, 
# but in production it will be handled mta.yaml start command)
if __name__ == "__main__":
    uvicorn.run("app.app:app", host=HOST, port=PORT, reload=DEBUG, log_config=None, workers=WORKERS)