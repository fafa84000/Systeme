from logging import basicConfig, ERROR, error
from config import LOG_FILE
from pprint import pprint

basicConfig(
    filename=LOG_FILE,
    level=ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s - File: %(filename)s - Line: %(lineno)d',
    filemode='a'
)

def log_error(exception):
    error(f"Exception occured: {exception}", exc_info=True)
    pprint(exception)