import logging.handlers

logging.basicConfig(level=logging.DEBUG)

log_path = 'log.txt'
open(log_path, 'w+')
log = logging.getLogger()

log.addHandler(
    logging.handlers.WatchedFileHandler(log_path)
)
