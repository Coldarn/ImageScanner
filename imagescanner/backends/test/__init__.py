import os
import Image

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
    def __init__(self, **kwargs):
        self._devices = []
 
    def __refresh__(self):
        self._devices = []
        scanner = Scanner('test-0', "Pyscan", "Test Device")
        self._devices.append(scanner)
    
    def get_scanner(self, id):
        self.__refresh__()

        for dev in self._devices:
            if dev.id == id: return dev

        return None

    def list_scanners(self):
        self.__refresh__()
        return self._devices

class Scanner(base.Scanner):  
    def __init__(self, id, manufacturer, name):
        self.id = id
        self.manufacturer = manufacturer
        self.name = name

    def __repr__(self):
        return "<%s: %s - %s>" % (self.id, self.manufacturer, self.name)
    
    def scan(self):
        imgpath = os.path.join(os.path.dirname(__file__), 'data', 'img1.tiff')
        return Image.open(imgpath)
