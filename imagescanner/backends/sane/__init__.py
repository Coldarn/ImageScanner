import sane

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
    def __init__(self):
        self._devices = []
 
    def _refresh(self):
        for scanner in self._devices:
            scanner.close()
        self._devices = []
        sane.exit()

        sane.init()
        devices = sane.get_devices()    
        for dev in devices: 
            id = "sane-%s" % len(self._devices)
            try:
                scanner = Scanner(id, dev[0], dev[1], dev[2], dev[3])
                self._devices.append(scanner)
            except:
                pass
    
    def getScanner(self, id):
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
        self._scanner = sane.open(device)

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self):
        return self._scanner.scan()
    
    def close(self):
        self._scanner.close()
    
    # TODO: Implement status
    def status(self):
        pass
