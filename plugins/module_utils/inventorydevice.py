class inventorydevice:
    def __init__(self):
        pass

    def resetvalidation(self):
        pass

    def validatehost(self, hostvars):
        if hostvars.get('prop_device') is None:
            return {'valid': True, 'message': 'device data is empty'}
        hosthost = hostvars['prop_device']
        if hosthost.get('vendor') is None:
            return {'valid': False, 'message': 'vendor is missing'}
        if hosthost.get('model') is None:
            return {'valid': False, 'message': 'model is missing'}
        return {'valid': True, 'message': 'device data is valid'}
