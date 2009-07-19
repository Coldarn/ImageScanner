import Image
from StringIO import StringIO
import twain

from imagescanner.backends import base

class ScannerCollection(base.ScannerCollection):
    def __init__(self):
        self.__devices = []
 	self.sm = None

    def __renewsm(self):
	if self.sm is not None:
            self.sm.destroy()
        self.sm = twain.SourceManager(0)

    def __refresh(self):
        for scanner in self.__devices:
            scanner.close()
        self.__devices = []
        self.__renewsm()
	
        devices = self.sm.GetSourceList()
        for dev in devices: 
            id = len(self.__devices)
            try:
                scanner = Scanner(id, dev)
                self.__devices.append(scanner)
            except Exception, e:
                pass
    
    def get(self, scanner_id):
        self.__refresh()
        id = int(scanner_id)
        for dev in self.__devices:
            if dev.id == id:
                return dev
        return None

    def list(self):
        self.__refresh()
        return tuple([scanner.info() for scanner in self.__devices])

class Scanner(base.Scanner):  
    def __init__(self, id, sourceName):
        self.id = id
	self.__sourceName = sourceName

        self.__open()
        self.__getIdentity()
	self.close()
	
    def __getIdentity(self):
	identity = self.__scanner.GetIdentity()
        self.name = identity['ProductName']
	self.manufacturer = identity['Manufacturer']
	self.description = ''

    def __open(self):
        self.__sm = twain.SourceManager(0)
        self.__scanner = self.__sm.OpenSource(self.__sourceName)
        self.__scanner.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, 200.0)

    def __str__(self):
        return '%s: %s' % (self.id, self.name)
    
    def scan(self):
	self.__open()
        self.__scanner.RequestAcquire(0, 0)
	info = self.__scanner.GetImageInfo()
	if info:
            (handle, more_to_come) = self.__scanner.XferImageNatively()
            strImage = twain.DIBToBMFile(handle)
            twain.GlobalHandleFree(handle)
	    self.close()
            return Image.open(StringIO(strImage))

    def info(self):
        return {'id': self.id, 
                'manufacturer': self.manufacturer, 
                'name': self.name}
   
    def close(self):
        self.__scanner.destroy()
	self.__sm.destroy()

