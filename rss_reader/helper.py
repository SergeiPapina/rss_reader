"""This module has main settings of an app."""
import logging
import os

from pathlib import Path
from datetime import datetime

from pydantic import BaseSettings

class Settings(BaseSettings):
     """Class, containing global settings od an app."""
     project_name = "rs-reader"
     data_dir = str(Path.home() / 'rss_data')

def set_log_file_name():
    """this method to format an easy-to-read file name for logging"""

    log_dir = str(Path.home() / 'rss_log')

    if not Path(log_dir).exists():
        os.mkdir(log_dir)

    curr_time = datetime.now()
    file_name = (
            f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}'
            + '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}'
            + '_' + f'{curr_time.time().second}' + 'rss_log.log'
    )
    return Path(log_dir, file_name)

settings = Settings()
log_path = set_log_file_name()
if not Path(settings.data_dir).exists():
    os.mkdir(settings.data_dir)


logger = logging.getLogger(settings.project_name)
logger.setLevel(logging.INFO)

logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger_stdout_handler = logging.StreamHandler()
logger_stdout_handler.setLevel(logging.WARNING)
logger_stdout_handler.setFormatter(logger_formatter)

logger_file_handler = logging.FileHandler(log_path)
logger_file_handler.setLevel(logging.INFO)
logger_file_handler.setFormatter(logger_formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stdout_handler)

