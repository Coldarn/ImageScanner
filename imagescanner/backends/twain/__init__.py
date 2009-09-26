import logging
from StringIO import StringIO

import Image
import twain
from imagescanner.backends import base

class ScannerManager(base.ScannerManager):
    
    def _refresh(self):
        self._devices = []
        src_manager = twain.SourceManager(0)
        devices = src_manager.GetSourceList()
        for dev in devices: 
            scanner_id = 'twain-%s' % len(self._devices)
            try:
                scanner = Scanner(scanner_id, dev)
                self._devices.append(scanner)
            except Exception, exc:
                # XXX: What should be here?
                # Debuging to try to find out
                logging.debug(exc)
        src_manager.destroy()

class Scanner(base.Scanner):  
    def __init__(self, scanner_id, source_name):
        self.id = scanner_id
        self._source_name = source_name

        self.name = None
        self.manufacturer = None
        self.description = None
        self._src_manager = None
        self._scanner = None
    
        self._open()
        self._get_identity()
        self._close()
    
    def _get_identity(self):
        identity = self._scanner.GetIdentity()
        self.name = identity.get('ProductName')
        self.manufacturer = identity.get('Manufacturer')
        self.description = None

    def _open(self):
        self._src_manager = twain.SourceManager(0)
        self._scanner = self._src_manager.OpenSource(self._source_name)
        self._scanner.SetCapability(twain.ICAP_YRESOLUTION, 
                                    twain.TWTY_FIX32, 200.0)

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self, dpi=200):
        self._open()
        self._scanner.RequestAcquire(0, 0)
        info = self._scanner.GetImageInfo()
        if info:
            (handle, more_to_come) = self._scanner.XferImageNatively()
            str_image = twain.DIBToBMFile(handle)
            twain.GlobalHandleFree(handle)
            self._close()
            return Image.open(StringIO(str_image))

        self._close()
        return None
    
    def _close(self):
        self._scanner.destroy()
        self._src_manager.destroy()

    def status(self):
        pass
