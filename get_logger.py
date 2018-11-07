from nk_logger import config_logger, get_logger as get_nk_logger

config_logger(level="INFO", prefix="croc")

def get_logger(file_name):
    logger = get_nk_logger(file_name)
    return logger
