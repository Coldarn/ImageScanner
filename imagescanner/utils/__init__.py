
def scanner_serializer(device):
    return {
        'id': device.id,
        'name': device.name,
        'manufacturer': getattr(device, 'manufacturer', None),
        'description': getattr(device, 'description', None),
    }

