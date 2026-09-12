import os
import configparser

import logging
logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print(f"ERROR: Root logger had no handlers. Logging unavailable in module {__name__}.")

class Settings:
    def __init__(self, ini_path):
        self.config = configparser.ConfigParser()
        self.config.read(ini_path)
        logger.info(f"Settings initialized from settings.ini file: {ini_path}")

    def get(self, section, key, env_key=None, fallback=None):
        env_var = env_key or key.upper()
        if env_var in os.environ:
            logger.debug(f"{env_var} taken from environment variables : {os.environ[env_var]}")
            return os.environ[env_var]
        if self.config.has_option(section, key):
            logger.debug(f"{key} taken from settings.ini : {self.config.get(section, key)}")
            return self.config.get(section, key)
        logger.debug(f"{key} not found in environment variables or settings.ini, using fallback: {fallback}")
        return fallback

'''
    SETTINGS_INI_PATH = "settings.ini"

    config = configparser.ConfigParser()
    config.read(SETTINGS_INI_PATH)
    
    APP_MODE = config.get("Main", "app_mode")
    HOST = get_config_value(config, APP_MODE, "server_host")
    PORT = int(get_config_value(config, APP_MODE, "server_port", fallback=5000))
'''