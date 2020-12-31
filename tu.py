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

# unit test flag
CHECK_FLAG_LEX = False
CHECK_FLAG_AST = False
CHECK_FLAG_CFG = False
CHECK_FLAG_SYMTAB = False
CHECK_FLAG_CALL_GRAPH = False
CHECK_FLAG_PASS = False
CHECK_FLAG_AS = False


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


def init_check_flag(check_flag):
    if check_flag == 1:
        global CHECK_FLAG_LEX
        CHECK_FLAG_LEX = True
    elif check_flag == 2:
        global CHECK_FLAG_AS
        CHECK_FLAG_AST = True
    elif check_flag == 3:
        global CHECK_FLAG_CFG
        CHECK_FLAG_CFG = True
    elif check_flag == 4:
        global CHECK_FLAG_SYMTAB
        CHECK_FLAG_SYMTAB = True
    elif check_flag == 5:
        global CHECK_FLAG_CALL_GRAPH
        CHECK_FLAG_CALL_GRAPH = True
    elif check_flag == 6:
        global CHECK_FLAG_PASS
        CHECK_FLAG_PASS = True
    else:
        global CHECK_FLAG_AS
        CHECK_FLAG_AS = True
