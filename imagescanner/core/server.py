import cjson
import imagescanner

from cStringIO import StringIO
from twisted.web import server
from twisted.web.xmlrpc import XMLRPC, Binary

class ScannerDevices(XMLRPC):

    def xmlrpc_list(self):
        device_list = imagescanner.list()
        return cjson.encode(device_list)

    def xmlrpc_scan(self, device_id):
        device = imagescanner.get(device_id)
        image = device.scan()
        image_data = StringIO()
        image.save(image_data, 'tiff')
        image_data.seek(0) 
        return Binary(image_data.read())

if __name__ == '__main__':
    from twisted.internet import reactor
    port = settings.SERVER_PORT
    
    root = ScannerDevice()
    reactor.listenTCP(port, server.Site(root))
    reactor.run()
