import cjson
from imagescanner import ImageScanner

from cStringIO import StringIO
from twisted.web import server
from twisted.web.xmlrpc import XMLRPC, Binary

class ScannerDevices(XMLRPC):

    def xmlrpc_listScanners(self):
        devices = ImageScanner().listScanners()
        serialized_devices = [self.serialize(device) for device in devices]
        return cjson.encode(serialized_devices)

    def xmlrpc_scan(self, device_id):
        image = ImageScanner().scan(device_id)
        if image is None:
            return None
        image_data = StringIO()
        image.save(image_data, 'tiff')
        image_data.seek(0) 
        return Binary(image_data.read())
    
    def serialize(self, device):
        return {
            'id': device.id,
            'name': device.name,
            'manufacturer': getattr(device, 'manufacturer', None),
            'description': getattr(device, 'description', None),
        }

def runserver(port):
    from twisted.internet import reactor
    
    root = ScannerDevices()
    reactor.listenTCP(port, server.Site(root))
    reactor.run()
