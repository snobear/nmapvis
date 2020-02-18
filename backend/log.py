"""Backend logging configuration"""
import logging

LOGFILE='/tmp/app.log'

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def setup_logging(level='info', log_to_terminal=False):
    lvl = level.lower()

    show_level_warning = False
    if lvl not in LEVELS:
        lvl_supplied = lvl
        lvl = 'info'
        show_level_warning = True

    log = logging.getLogger()
    log.setLevel(LEVELS[lvl])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log to file
    fh = logging.FileHandler(LOGFILE)
    fh.setLevel(LEVELS[lvl])
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # log to terminal (for dev)
    if log_to_terminal:
        ch = logging.StreamHandler()
        ch.setLevel(LEVELS[lvl])
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if show_level_warning:
        log.warning("%s not a valid log level. defaulting to level=info" % lvl_supplied)

    return log
