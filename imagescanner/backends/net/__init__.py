import xmlrpclib
import socket
import logging
from cStringIO import StringIO

import Image
import cjson
from imagescanner import settings
from imagescanner.backends import base

class ScannerManager(base.ScannerManager):

    def __init__(self, **kwargs):
        super(ScannerManager, self).__init__(**kwargs)
        remote_hosts = kwargs.get('remote_hosts', tuple())       
 
        self._proxies = []
        for host in remote_hosts:
            proxy = xmlrpclib.ServerProxy("http://%s/" % host, allow_none=True)
            self._proxies.append(proxy)

    def _refresh(self):
        logging.info('Reloading remote device information')
        self._devices = []
        for proxy in self._proxies:
            # TODO: Redo it without accessing protected members
            remote_host = proxy._ServerProxy__host
            try:
                response = proxy.list_scanners()
            except socket.error:
                logging.error('Connection refused when trying to list '
                              'scanners in %s [skiping]', remote_host)
                continue
            logging.debug('JSON answer from %s: %s', remote_host, response)
            
            scanner_list = cjson.decode(response)
            for scanner_info in scanner_list:
                scanner_info.update({'proxy': proxy})
                scanner = Scanner(**scanner_info)
                self._devices.append(scanner)
        logging.debug('Remote devices loaded: %s', self._devices)
 
class Scanner(base.Scanner):

    def __init__(self, **kwargs):
        # Different hosts can have the same id, so the host need to be part of
        #   the scanner id
        scanner_id = kwargs.get('id', None)
        proxy = kwargs.get('proxy', None)
        remote_host = proxy._ServerProxy__host

        self.id = "%s/%s" % (remote_host, scanner_id)
        self._remote_id = scanner_id
        self.name = kwargs.get('name', None)
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
        pass
