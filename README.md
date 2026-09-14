# kyma-lab
Kyma runtime test 

## local python development

Prepare environment:
```
/usr/local/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run fastAPI service
```
debug: python3 -m app.app
uvicorn app.app:app --host 0.0.0.0 --port 3000
```

## Project Structure

```
kyma-lab/
├── .git/                # Git version control
├── .gitignore           # Git ignore rules
├── .idea/               # IDE configuration
├── .venv/               # Python virtual environment
├── README.md            # This file
├── how_to_kyma.txt      # KYMA documentation
├── py_test/             # Main application directory
│   ├── .dockerignore    # Docker ignore rules
│   ├── Dockerfile       # Docker image configuration
│   ├── requirements.in  # Base requirements
│   ├── requirements.txt # Pinned dependencies
│   ├── settings.ini     # Application settings
│   └── app/             # Application source code
│       ├── __init__.py  # Package init
│       ├── app.py       # Main application entry point
│       ├── middleware.py # Middleware components
│       ├── routes/      # API route definitions
│       │   ├── __init__.py
│       │   └── common/  # Common route utilities
│       ├── settings.py  # Application settings
│       ├── settings_tools.py  # Settings tools
│       ├── static/      # Static assets
│       │   ├── favicon.ico
│       │   └── logo.png
│       ├── themes/      # Theme configurations
│       │   ├── __init__.py
│       │   ├── color_palette.py
│       │   ├── dark_theme_preview.html
│       │   ├── light_theme_preview.html
│       │   └── logo.png
│       ├── utils/       # Utility modules
│       │   ├── __init__.py
│       │   ├── env_vars.py
│       │   └── module_logger.py
│       └── assets/      # Additional assets
│           └── .env
│       └── __pycache__/ # Python compiled bytecode
├── .DS_Store           # macOS directory metadata
└── .gitignore          # Git ignore rules
└──  deployment.yaml    # deployment configuration
```
