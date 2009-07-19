import sane
import logging

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
    def __init__(self, **kwargs):
        self._devices = []
 
    def _refresh(self):
        self._devices = []
        
        sane.init()
        devices = sane.get_devices()    
        for dev in devices: 
            id = 'sane-%s' % len(self._devices)
            try:
                scanner = Scanner(id, dev[0], dev[1], dev[2], dev[3])
                self._devices.append(scanner)
            except Exception, e:
                # XXX: Which exception should be here?
                # Logging to try to figure it out
                logging.debug(e)
        sane.exit()
    
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
    def __init__(self, id, device, manufacturer, name, description):
        self.id = id
        self.manufacturer = manufacturer
        self.name = name
        self.description = description
        self._device = device

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self):
        sane.init()
        scanner = sane.open(self._device)
        image = scanner.scan()
        scanner.close()
        sane.exit()

        return image
