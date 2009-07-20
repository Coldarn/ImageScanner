import xmlrpclib
import socket
import logging
from cStringIO import StringIO

import Image
import cjson
from imagescanner import settings
from imagescanner.backends import base

class ScannerManager(base.ScannerManager):

    def __init__(self, remote_hosts=(), **kwargs):
        self._devices = []
        
        self._proxies = []
        for host in remote_hosts:
            proxy = xmlrpclib.ServerProxy("http://%s/" % host, allow_none=True)
            self._proxies.append(proxy)
        
    def getScanner(self, id):
        self._refresh()
        for dev in self._devices:
            if dev.id == id:
                return dev
        return None
 
    def listScanners(self):
        self._refresh()
        return self._devices

    def _refresh(self):
        logging.debug('Reloading remote device information')
        self._devices = []
        for proxy in self._proxies:
            remote_host = proxy._ServerProxy__host
            try:
                response = proxy.listScanners()
            except socket.error:
                logging.error('Connection refused when trying to list '
                              'scanners in %s [skiping]' % remote_host)
                continue
            logging.debug('JSON answer from %s: %s' % (remote_host, response))
            
            scanner_list = cjson.decode(response)
            for scanner_info in scanner_list:
                scanner = Scanner(proxy, **scanner_info)
                self._devices.append(scanner)
        logging.debug('Remote devices loaded: %s' % self._devices)
 
class Scanner(object):

    def __init__(self, proxy, **kwargs):
        # Different hosts can have the same id, so the host need to be part of
        #   the scanner id
        remote_host = proxy._ServerProxy__host
        self.id = "%s/%s" % (remote_host, kwargs['id'])
        self._remote_id = kwargs['id']
        self.name = kwargs['name']
        self.manufacturer = kwargs.get('manufacturer', None)
        self.description = kwargs.get('description', None)
        self._proxy = proxy

    def scan(self, dpi=200):
        binary = self._proxy.scan(self._remote_id)
        if binary is None:
            return None

        image_data = StringIO()
        image_data.write(binary.data)
        image_data.seek(0)
        return Image.open(image_data)
    
    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)

    def status(self):
        # TODO: Define standard status
        raise NotImplementedError