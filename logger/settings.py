from loguru import logger

logger.add('logger.log', format='{time} || {level} || IN: {message}', 
           rotation='2 MB', enqueue=True)