import logging

LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        # logging.StreamHandler() # terminal
    ]
)

def get_logger(name:str):
    return logging.getLogger(name)