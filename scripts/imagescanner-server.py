#!/usr/bin/env python

import sys
import logging
from imagescanner.core import server
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", default=8000,
                  help="server port (default: 8000)")

(options, args) = parser.parse_args()

port = int(options.port)

logging.info('starting imagescanner server on port %s' % port)
logging.info('waiting for connections...')
server.run(port)

