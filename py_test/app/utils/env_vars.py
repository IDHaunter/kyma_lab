import os
import logging

logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print("ERROR: Root logger had no handlers. Logging unavailable.")

def get_value_from_environment(env_var_name: str, env_var_prefix: str, replace_none_value: str, hidden: bool = False):
    full_env_var_name = f"{env_var_prefix.upper()}_{env_var_name.upper()}"

    try:
        env_var_value = os.getenv(full_env_var_name)

        if env_var_value is not None:
            logger.debug(
                f"Environment variable '{full_env_var_name}' exists. Taking value: "
                f"{env_var_value if not hidden else f'<len:{len(env_var_value)}>'}"
            )

        else:
            logger.warning(f"Environment variable '{full_env_var_name}' does not exist.")
            env_var_value = replace_none_value
            logger.debug(f"{full_env_var_name}: {env_var_value}")

        return env_var_value

    except Exception as e:
        logger.error(f"An error occurred while trying to get the environment variable '{full_env_var_name}': {e}")
        logger.error(f" - {full_env_var_name}: None")
        return None