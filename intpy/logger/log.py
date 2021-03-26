import datetime


def _log(mode, message):
    print("[{2}][{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message, mode))


def debug(message):
    _log("DEBUG", message)


def error(message):
    _log("ERROR", message)


def warn(message):
    _log("WARN ", message)
