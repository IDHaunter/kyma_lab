from pathlib import Path
from dotenv import load_dotenv

current_module_directory = Path(__file__).resolve().parent
parent_directory = current_module_directory.parent

# ----------------
# PATHS
# ----------------

SETTINGS_INI_PATH = current_module_directory.parent / 'settings.ini'
LOGS_DIR = current_module_directory / 'logs'          # logs dir
UPLOAD_DIR = current_module_directory / 'tmp'         # dir for temporary files
ASSETS_DIR = current_module_directory / 'assets'      # dir for persistent files
DOTENV_PATH = ASSETS_DIR / '.env'                     # environmental variables file

# ----------------
# APP_MODE AND LOAD VARIABLES FROM .ENV
# ----------------

import configparser

config = configparser.ConfigParser()
config.read(SETTINGS_INI_PATH)
APP_MODE = config['Main']['app_mode']

load_dotenv(DOTENV_PATH)

# ----------------
# VERSION AND APP INFO
# ----------------

APP_NAME = 'py_test'
APP_VER = {'ver': '0.0.1',
           'date': '2026.09.12',
           'info': 'Initial version'}

# ----------------
# LOGGER
# ----------------

from app.utils.module_logger import configure_logging, get_logger
LOG_LEVEL_NAME = configure_logging()
logger = get_logger(__name__)


logger.info(f"LOG LEVEL NAME: {LOG_LEVEL_NAME}")
logger.info(f"APP MODE: {APP_MODE}")

# ----------------
# SETTINGS.INI
# ----------------

from app.settings_tools import Settings

settings = Settings(SETTINGS_INI_PATH)
DEBUG = settings.get(APP_MODE, 'debug_mode')
HOST = settings.get(APP_MODE, "server_host")
PORT = int(settings.get(APP_MODE, "server_port", fallback=3000))
WORKERS = int(settings.get(APP_MODE, "workers", fallback=1))

EXEC_TIME = DEBUG

# ----------------
# Read environment variables
# ----------------  

from app.utils.env_vars import get_value_from_environment
LOG_LEVEL = get_value_from_environment(
    env_var_name='LOG_LEVEL',
    env_var_prefix=APP_NAME,
    replace_none_value= 'DEBUG',
    hidden = False)