import time
import socket
import logging
import xmlrpclib
from cStringIO import StringIO

import Image
import cjson
from autoconnect import UdpReceiver
from imagescanner import settings
from imagescanner.backends import base

SEARCH_PORT = 3244
SEARCH_TIMEOUT = 5

class ScannerManager(base.ScannerManager):

    def __init__(self, **kwargs):
        super(ScannerManager, self).__init__(**kwargs)
        self.remote_hosts = kwargs.get('remote_hosts', list())       
 	
        if kwargs.get('remote_search', True):
            self._search_for_remote_devices()

        self._proxies = []
        for host in self.remote_hosts:
            proxy = xmlrpclib.ServerProxy("http://%s/" % host, allow_none=True)
            self._proxies.append(proxy)


    def _search_for_remote_devices(self):
        """Wait for broadcasted messages from remote ImageScanners.
        
        Listen in SEARCH_PORT waiting for broadcasted messages 
        containing the connection information (IP address and port) 
        that this backend will use to access the remote device. 
        
        The variable SEARCH_TIMEOUT is used to set timeout of each 
        one of the connections. Everytime a new device is discovered 
        the timeout is reset.
        
        """

        logging.debug('Waiting for remote scanners')
        udpr = UdpReceiver()
        
        wait_for_remote_devices = True
        time_last_found = 0
        while wait_for_remote_devices:
            # Wait for a broadcast message
            try:
                encoded_msg, socket_addr = udpr.receive(port=SEARCH_PORT, 
                                                        timeout=SEARCH_TIMEOUT)
            except socket.timeout:
                # in case of timeout stop searching
                msg = ('Stop searching for for devices. '
                       'Connection timeout (%s seconds)' % SEARCH_TIMEOUT)
                logging.debug(msg)
                wait_for_remote_devices = False
                return 
            
            msg = cjson.decode(encoded_msg)
            ipaddr = msg.get('ip')
        
            # If the IP address is generic or not set use the 
            #   address which the broadcast message came from
            if ipaddr == '0.0.0.0' or ipaddr is None:
                ipaddr = socket_addr[0]
    
            # Check if the port was set in the request
            if msg.get('port') is not None:
                remote_device_addr = "%s:%s" % (ipaddr, msg['port'])
                
                # Check if the device wasn't discovered previously
                if remote_device_addr not in self.remote_hosts:
                    logging.debug('Remote ImageScanner found at %s' % 
                                                    remote_device_addr)
                    # We are good! 
                    #   just add the device to the list and set 
                    #   the time_last_found to now
                    self.remote_hosts.append(remote_device_addr)
                    time_last_found = time.time()
                    logging.debug('Setting time_last_found to %s' % 
                                                      time_last_found)
            
            # Stop searching if the last device was discovered more than
            #   SEARCH_TIMEOUT seconds ago 
            time_now = time.time() 
            if int(time_now - time_last_found) > SEARCH_TIMEOUT:
                logging.debug('Time now: %s' % time_now)
                logging.debug('Last found at: %s' % time_last_found)
                wait_for_remote_devices = False


    def _refresh(self):
        logging.info('Reloading remote devices information')
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
