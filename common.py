import logging
from config import *

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

fh = logging.FileHandler(LOG_FILE)
fh.setLevel(LOG_LEVEL)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
ch.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(ch)
