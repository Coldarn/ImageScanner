"""Abstract base classes"""

class ScannerManager(object):

    def getScanner(self, id):
        """Return a scanner with the given ID or None if not found"""
        raise NotImplementedError

    def listScanners(self):
        """Return a list with  all the available devices"""
        raise NotImplementedError

class Scanner(object):
    """Abstract Scanner class"""

    def __init__(self):
        raise NotImplementedError

    def scan(self, dpi=200):
        """Scan a new image using the given DPI and returns a PIL object"""
        raise NotImplementedError

    def status(self):
        """Get device status"""
        # TODO: Define standard status
        raise NotImplementedError
