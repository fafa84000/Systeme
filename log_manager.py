from logging import basicConfig, ERROR, error
from config import LOG_FILE

basicConfig(
    filename=LOG_FILE,
    level=ERROR,
    format='\n%(asctime)s - %(levelname)s - %(message)s - File: %(filename)s - Line: %(lineno)d'
)

def log_error(exception):
    error(f"Exception occured: {exception}", exc_info=True)