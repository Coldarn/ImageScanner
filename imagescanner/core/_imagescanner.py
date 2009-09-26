import os
import logging

from imagescanner import settings
from imagescanner.utils.importlib import import_module

POSIX_BACKEND = 'imagescanner.backends.sane'
NT_BACKEND = 'imagescanner.backends.twain'
NETWORK_BACKEND = 'imagescanner.backends.net'
TEST_BACKEND = 'imagescanner.backends.test'

BACKENDS = getattr(settings, 'BACKENDS', None)

class ImageScanner(object):
    def __init__(self, **kwargs):
        self.managers = []
        backends = []

        # Enable default backend for each system
        if os.name == 'posix':
            logging.debug('Posix backend enabled (%s)', POSIX_BACKEND)
            backends.append(POSIX_BACKEND)
        elif os.name == 'nt':
            logging.debug('NT backend enabled (%s)', NT_BACKEND)
            backends.append(NT_BACKEND)
        
        # Check if we should load the test backend
        if hasattr(settings, 'ENABLE_TEST_BACKEND'):
            if settings.ENABLE_TEST_BACKEND:
                logging.debug('Test backend enabled (%s)', TEST_BACKEND)
                backends.append(TEST_BACKEND)
        
        # If trying to scan using a remote host enable network backend
        if kwargs.get('remote_hosts'):
            logging.debug('Network backend enabled (%s)', NETWORK_BACKEND)
            backends.append(NETWORK_BACKEND)

        # Check if the user has own backends defined
        if BACKENDS is not None:
            logging.debug('Adding user backends (%s)', BACKENDS)
            backends.extend(BACKENDS)
        
        for backend in backends:    
            try:
                logging.debug('Importing %s', backend)
                backend_module = import_module(backend)
            except Exception, exc:
                logging.warning('Error importing %s [skiping]', backend)
                logging.warning(exc)
                # Could not import, so go to the next backend 
                continue

            try:
                manager = backend_module.ScannerManager(**kwargs)
            except AttributeError:
                logging.error('Backend %s does not implement '
                              'ScannerManager class [skiping]', backend)
                # Backend not implement the required API, so skip it
                continue 
        
            self.managers.append(manager)

    def list_scanners(self):
        """List all devices for all the backends available"""
        logging.debug('Looking for all scanner devices') 
        scanners = []
        for manager in self.managers:
            scanners.extend(manager.list_scanners())
       
        logging.debug('Found scanners: %s', scanners) 
        return scanners

    def get_scanner(self, scanner_id):
        """Get the device with the given ID"""
        logging.debug('Looking for scanner with id: %s', scanner_id)
        scanner = None
        for manager in self.managers:
            scanner = manager.get_scanner(scanner_id)
            if scanner is not None:
                logging.debug('Scanner %s found', scanner_id)
                return scanner
        logging.debug('Scanner %s not found', scanner_id)

    def scan(self, scanner_id, **kwargs):
        """Shortcut for scanning without get the device"""

        logging.debug('Trying to scan using: %s and %s', scanner_id, kwargs)
        scanner = self.get_scanner(scanner_id)
        if scanner is not None:
            return scanner.scan(**kwargs)
       
        logging.info('Scan failed. Scanner %s not found', scanner_id)
