
from imagescanner.core._imagescanner import ImageScanner

# Configure the python logging using the custom handler
from imagescanner.utils.logger import config_logger
config_logger()
del config_logger
