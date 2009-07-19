import logging
from StringIO import StringIO

import Image
import twain
from imagescanner.backends import base

class ScannerManager(base.ScannerManager):
    def __init__(self, **kwargs):
        self._devices = []
        self.sm = None

    def _refresh(self):
        self.devices = []
        self.sm = twain.SourceManager(0)
        devices = self.sm.GetSourceList()
        for dev in devices: 
            id = 'twain-%s' % len(self._devices)
            try:
                scanner = Scanner(id, dev)
                self._devices.append(scanner)
            except Exception, e:
                # XXX: What should be here?
                # Debuging to try to find out
                logging.debug(e)
        self.sm.destroy()
    
    def getScanner(self, id):
        self._refresh()
        for dev in self._devices:
            if dev.id == id:
                return dev
        return None

    def listScanners(self):
        self._refresh()
        return self._devices

class Scanner(base.Scanner):  
    def __init__(self, id, sourceName):
        self.id = id
        self._sourceName = sourceName

        self._open()
        self._getIdentity()
        self._close()
    
    def _getIdentity(self):
        identity = self._scanner.GetIdentity()
        self.name = identity.get('ProductName')
        self.manufacturer = identity.get('Manufacturer')
        self.description = None

    def _open(self):
        self._sm = twain.SourceManager(0)
        self._scanner = self._sm.OpenSource(self._sourceName)
        self._scanner.SetCapability(twain.ICAP_YRESOLUTION, 
                                    twain.TWTY_FIX32, 200.0)

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self):
        self._open()
        self._scanner.RequestAcquire(0, 0)
        info = self._scanner.GetImageInfo()
        if info:
            (handle, more_to_come) = self._scanner.XferImageNatively()
            strImage = twain.DIBToBMFile(handle)
            twain.GlobalHandleFree(handle)
            self._close()
            return Image.open(StringIO(strImage))

        self._close()
        return None
    
    def _close(self):
        self._scanner.destroy()
        self._sm.destroy()

