import os
import Image

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
 
    def _refresh(self):
        self._devices = []
        scanner = Scanner('test-0', "Pyscan", "Test Device")
        self._devices.append(scanner)

class Scanner(base.Scanner):  
    def __init__(self, scanner_id, manufacturer, name):
        self.id = scanner_id
        self.manufacturer = manufacturer
        self.name = name

    def __repr__(self):
        return "<%s: %s - %s>" % (self.id, self.manufacturer, self.name)
    
    def scan(self, dpi=200):
        imgpath = os.path.join(os.path.dirname(__file__), 'data', 'img1.tiff')
        return Image.open(imgpath)

    def status(self):
        pass
