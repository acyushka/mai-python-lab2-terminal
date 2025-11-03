from loguru import logger

def log_shell(line):
    if line:
        logger.info(line)
    return line