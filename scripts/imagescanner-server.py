from twisted.application import internet, service
from twisted.web import server
from imagescanner.core.server import ScannerDevices
from imagescanner import settings

port = settings.SERVER_PORT
factory = ScannerDevices()

# this is the important bit
application = service.Application('scanner-device')
scanningService = internet.TCPServer(port, server.Site(factory))
# add the service to the application
scanningService.setServiceParent(application)
