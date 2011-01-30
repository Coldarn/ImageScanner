import xmlrpclib
from cStringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

import cjson
from imagescanner import ImageScanner
from imagescanner.utils import scanner_serializer


def list_scanners():
    devices = ImageScanner(remote_search=False).list_scanners()
    serialized_devices = [scanner_serializer(device) for device in devices]
    return cjson.encode(serialized_devices)


def scan(device_id):
    image = ImageScanner(remote_search=False).scan(device_id)
    if image is None:
        return None
    image_data = StringIO()
    image.save(image_data, 'tiff')
    image_data.seek(0) 
    return xmlrpclib.Binary(image_data.read())

    
class RequestHandler(SimpleXMLRPCRequestHandler):
     rpc_paths = ('/RPC2',)


def run(listen_address, port):
    server = SimpleXMLRPCServer((listen_address, port), 
                                requestHandler=RequestHandler)

    server.register_introspection_functions()
    server.register_function(list_scanners)
    server.register_function(scan)
    server.serve_forever()