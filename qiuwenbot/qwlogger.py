import logging
qwlogger = logging.getLogger("QiuwenBot")
qwlogger.setLevel(logging.INFO)
ch = logging.StreamHandler()
qwlogger.addHandler(ch)

__all__ = ['qwlogger']
