import os, logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import dotenv_values
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG = dotenv_values(os.path.join(BASE_DIR, '.env.prod'))

formatter = logging.Formatter('[%(asctime)s] [%(module)s]- [%(levelname)s] - [%(funcName)s: %(lineno)d] - %(message)s')
handler = TimedRotatingFileHandler(
    filename=f'logs/log.log',
    encoding='utf-8',
    when='D',
    backupCount=10,
)
handler.setFormatter(formatter)
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
LOGGER = logger

