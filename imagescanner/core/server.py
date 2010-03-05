import cjson

from cStringIO import StringIO
from twisted.web import server
from twisted.web.xmlrpc import XMLRPC, Binary

from imagescanner import ImageScanner
from imagescanner.utils import scanner_serializer

class ScannerDevices(XMLRPC):

    def xmlrpc_list_scanners(self):
        devices = ImageScanner().list_scanners()
        serialized_devices = [scanner_serializer(device) for device in devices]
        return cjson.encode(serialized_devices)

    def xmlrpc_scan(self, device_id):
        image = ImageScanner().scan(device_id)
        if image is None:
            return None
        image_data = StringIO()
        image.save(image_data, 'tiff')
        image_data.seek(0) 
        return Binary(image_data.read())
    
def run(port):
    from twisted.internet import reactor
    
    root = ScannerDevices()
    reactor.listenTCP(port, server.Site(root))
    reactor.run()
