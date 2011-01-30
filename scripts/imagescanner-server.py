#!/usr/bin/env python

import sys
import logging
import socket
import cjson
from imagescanner.core import server
from optparse import OptionParser
from autoconnect import UdpBroadcaster

XMLRPC_SERVER_PORT = 3244
DEFAULT_BROADCAST_IP = socket.gethostbyname('<broadcast>')
DEFAULT_BROADCAST_PORT = XMLRPC_SERVER_PORT
BROADCAST_INTERVAL = 1

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", 
                  default=XMLRPC_SERVER_PORT, type="int", 
                  help=("ImageScanner TCP port. "
                       "(default: %s)" % XMLRPC_SERVER_PORT))
parser.add_option("-l", "--listen-address", dest="listen_address", 
                  default='0.0.0.0', 
                  help=("Inferface listening to connections. Set it to " 
                        "0.0.0.0 to use all interfaces. (default: 0.0.0.0)"))
parser.add_option("-b", "--broadcast", dest="broadcast", 
                  default=DEFAULT_BROADCAST_IP, 
                  help=("Broadcast server info on that address. "
                        "Set it to None to disable broadcast. "
                        "(default: %s)" % DEFAULT_BROADCAST_IP))
parser.add_option("--broadcast-port", dest="broadcast_port", 
                  default=DEFAULT_BROADCAST_PORT, 
                  help=("Broadcast server info on that UDP port. "
                        "Clients must be listening on the same port. "
                        "(default: %s)" % DEFAULT_BROADCAST_PORT))

(options, args) = parser.parse_args()

if options.broadcast:
    logging.info('broadcasting server address to %s:%s' % (
                                                    options.broadcast, 
                                                    DEFAULT_BROADCAST_PORT))
    broadcaster = UdpBroadcaster(broadcast_address=options.broadcast, 
                                 broadcast_period=BROADCAST_INTERVAL)
    msg = {
        'app': 'ImageScannerServer',
        'port': options.port,
        'ip': options.listen_address,
    }
    encoded_msg = cjson.encode(msg) 
    msg = 'broadcasting message: %s' % encoded_msg
    logging.debug(msg)
    broadcaster.start(encoded_msg, [DEFAULT_BROADCAST_PORT])

logging.info('starting imagescanner server on port %s' % options.port)
logging.info('waiting for connections...')
server.run(options.port)

