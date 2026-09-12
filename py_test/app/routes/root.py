from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.settings import APP_NAME, APP_VER, LOG_LEVEL_NAME
from app.themes.color_palette import LightThemePalette, DarkThemePalette
from app.routes.common.responses import ResponseMessages
from app.middleware import PUBLIC_ENDPOINTS
import logging

logger = logging.getLogger(__name__)

# Create FastAPI router
router = APIRouter(tags=["root"])

if not PUBLIC_ENDPOINTS:
    html_public_endpoints = '<p>Public endpoints are unavailable</p>'
else:
    items = ''.join(f'<li>{endpoint}</li>' for endpoint in PUBLIC_ENDPOINTS)
    html_public_endpoints = f'<p>List of public endpoints:</p><ul>{items}</ul>'

@router.get("/",
            summary="Common Information",
            description="Root endpoint - returns HTML page with common information.",
            response_class=HTMLResponse)
async def root():
    try:
        logo_url = "/static/logo.png"
        html_content = f'''
            <html>
                <head>
                    <title>Niflheim: {APP_NAME} service</title>
                <style>
                    :root {{
                        --color-bg: {LightThemePalette.COLOR_BACKGROUND};
                        --color-text: {LightThemePalette.COLOR_TEXT};
                        --color-container-bg: {LightThemePalette.COLOR_CONTAINER};
                        --color-footer: {LightThemePalette.COLOR_TEXT};
                        --color-h1: {LightThemePalette.COLOR_TEXT_HIGHLIGHTED};
                        --color-accent: {LightThemePalette.COLOR_TEXT_HIGHLIGHTED};
                    }}

                    @media (prefers-color-scheme: dark) {{
                        :root {{
                            --color-bg: {DarkThemePalette.COLOR_BACKGROUND};
                            --color-text: {DarkThemePalette.COLOR_TEXT};
                            --color-container-bg: {DarkThemePalette.COLOR_CONTAINER};
                            --color-footer: {DarkThemePalette.COLOR_TEXT};
                            --color-h1: {DarkThemePalette.COLOR_TEXT_HIGHLIGHTED};
                            --color-accent: {DarkThemePalette.COLOR_TEXT_HIGHLIGHTED};
                        }}
                    }}

                    body {{
                        font-family: Arial, sans-serif;
                        background-color: var(--color-bg);
                        color: var(--color-text);
                        padding: 20px;
                    }}
                    .container {{
                        background-color: var(--color-container-bg);
                        padding: 30px;
                        border-radius: 10px;
                        max-width: 800px;
                        margin: auto;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                    }}
                    h1 {{
                        color: var(--color-h1);
                    }}
                    .footer {{
                        margin-top: 40px;
                        font-size: 18px;
                        color: var(--color-footer);
                    }}
                    .footer img {{
                        height: 30px;
                        vertical-align: middle;
                        margin: 0 1px;
                    }}
                </style>

                </head>
                <body>
                    <div class="container">
                        <h1>Niflheim: {APP_NAME} service</h1>
                        <p>version : {APP_VER['ver']} </p>
                        <p>date : {APP_VER['date']} </p>
                        <p>info : {APP_VER['info']} </p>
                        <p>logging level: <span style="color: var(--color-accent);">{LOG_LEVEL_NAME}</span></p>
                        {html_public_endpoints}
                        <div class="footer">
                            Plant your <img src="{logo_url}" alt="o">wn tree of knowledge
                        </div>
                    </div>
                </body>
            </html>
        '''
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        return ResponseMessages.error_500(str(e))