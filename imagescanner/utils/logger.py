                                                                    
import logging
from imagescanner import settings

class CustomStreamHandler(logging.StreamHandler, object):
    def emit(self, record):
        record.msg = '%s: %s' % (record.levelname, record.msg)
        super(CustomStreamHandler, self).emit(record)

def config_logger():
    handler = CustomStreamHandler()
    logging.root.setLevel(settings.LOGGING_LEVEL)
    logging.root.addHandler(handler)
