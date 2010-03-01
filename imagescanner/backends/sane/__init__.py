import sane

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
 
    def _refresh(self):
        self._devices = []
        
        sane.init()
        devices = sane.get_devices()    
        for dev in devices:
            # Check if sane is able to open this device, if not just skip
            try:
                scanner = sane.open(dev[0])
                scanner.close()
            except:
                continue 
                                
            scanner_id = 'sane-%s' % len(self._devices)
            scanner = Scanner(scanner_id, dev[0], dev[1], dev[2], dev[3])
            self._devices.append(scanner)

        sane.exit()

class Scanner(base.Scanner):  
    def __init__(self, scanner_id, device, manufacturer, name, description):
        self.id = scanner_id
        self.manufacturer = manufacturer
        self.name = name
        self.description = description
        self._device = device

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self, dpi=200):
        sane.init()
        scanner = sane.open(self._device)
        image = scanner.scan()
        scanner.close()
        sane.exit()

        return image
