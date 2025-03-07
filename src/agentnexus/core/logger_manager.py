import logging
import os

from agentnexus.core.config_manager import ConfigManager

class LoggerManager:
    """Centralized logger for all agents with global logging control."""

    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "agent_logs.log")

    @staticmethod
    def get_logger(name):
        """Returns a logger instance with logging enabled/disabled based on ConfigManager."""
        config = ConfigManager.get_config()
        log_enabled = config.get("enable_logging", True)  

        logger = logging.getLogger(name)

        if not log_enabled:
            logger.setLevel(logging.CRITICAL)
            return logger

        if not os.path.exists(LoggerManager.LOG_DIR):
            os.makedirs(LoggerManager.LOG_DIR)

        if not logger.hasHandlers():  
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            file_handler = logging.FileHandler(LoggerManager.LOG_FILE)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger
