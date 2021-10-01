import logging
import pathlib

ROOT_PATH = pathlib.Path(__file__).parents[1]
LOG_DIR = ROOT_PATH.joinpath("logs")
if not LOG_DIR.exists():
    LOG_DIR.mkdir()
WORD_DIR = ROOT_PATH.joinpath("words")
if not WORD_DIR.exists():
    WORD_DIR.mkdir()

logger = logging.getLogger('exception')

formatter = logging.Formatter(
    "\n%(asctime)s - %(filename)s - %(levelname)s \n %(message)s")
log_file_handler = logging.FileHandler(
    LOG_DIR.joinpath('exception.txt'), encoding='utf-8')
log_file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_file_handler)
