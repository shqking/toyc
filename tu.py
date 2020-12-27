import logging
from logging import handlers

# global metadata
src_file_name = ''
as_file_name = ''
log_file_name = ''
toks = list()
ast = list()
symtab = list()
logger = logging.getLogger("toyc")

PHASE_TAG_STR = "====================================="
SUBPHASE_TAG_STR = "-------------------------------------"


def init_logger():
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logFilePath = log_file_name
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=logFilePath, when='midnight', backupCount=30)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
