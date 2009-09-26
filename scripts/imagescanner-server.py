from twisted.application import internet, service
from twisted.web import server
from imagescanner.core.server import ScannerDevices
from imagescanner import settings

PORT = getattr(settings, 'SERVER_PORT', 8000)

factory = ScannerDevices()

# this is the important bit
application = service.Application('scanner-device')
scanningService = internet.TCPServer(PORT, server.Site(factory))
# add the service to the application
scanningService.setServiceParent(application)
