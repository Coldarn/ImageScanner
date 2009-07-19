import logging
from imagescanner import settings
from imagescanner.utils.importlib import import_module

DEFAULT_BACKENDS = ['imagescanner.backends.sane', 
                    'imagescanner.backends.twain']
NETWORK_BACKENDS = ['imagescanner.backends.net']
TEST_BACKEND = 'imagescanner.backends.test'

class ImageScanner(object):
    def __init__(self):
        self.managers = []
        
        backends = []
        backends.extend(DEFAULT_BACKENDS)
        
        # Check if we should load the test backend
        if hasattr(settings, 'ENABLE_TEST_BACKEND'):
            if settings.ENABLE_TEST_BACKEND:
                logging.debug('Test backend enabled (%s)' % TEST_BACKEND)
                backends.append(TEST_BACKEND)
        
        # Check if the user has own backends defined
        if hasattr(settings, 'BACKENDS'):
            if isinstance(settings.BACKENDS, list):
                logging.debug('Adding user backends (%s)' % settings.BACKENDS)
                backends.extend(settings.BACKENDS)
        
        for backend in backends:    
            try:
                logging.debug('Importing %s' % backend)
                backend_module = import_module(backend)
            except:
                logging.warning('Error importing %s [skiping]' % backend)
                # Could not import, so go to the next backend 
                continue

            try:
                manager = backend_module.ScannerManager()
            except AttributeError:
                logging.error('Backend %s does not implement '
                              'ScannerManager class [skiping]' % backend)
                # Backend not implement the required API, so skip it
                continue 
        
            self.managers.append(manager)

    def listScanners(self):
        """List all devices for all the backends available"""
        scanners = []
        for manager in self.managers:
            scanners.extend(manager.listScanners())
        
        return scanners

    def getScanner(self, id):
        """Get the device with the given ID"""
        scanner = None
        for manager in self.managers:
            scanner = manager.getScanner(id)
            if scanner is not None:
                return scanner

    def scan(self, id, **kwargs):
        """Shortcut for scanning without get the device"""
        scanner = self.getScanner(id)
        return scanner.scan(**kwargs)

