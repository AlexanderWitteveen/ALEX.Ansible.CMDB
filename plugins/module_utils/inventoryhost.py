import uuid


class inventoryhost:
    def __init__(self):
        self.hostnames = []

    def resetvalidation(self):
        self.hostnames = []

    def validatehost(self, hostvars):
        if hostvars.get('prop_host') is None:
            return {'valid': False, 'message': 'host data is empty'}
        hosthost = hostvars['prop_host']
        if hosthost.get('hostname') is None:
            return {'valid': False, 'message': 'hostname is missing'}
        hostname = hosthost['hostname']
        if hosthost.get('ipaddress') is None:
            return {'valid': False, 'message': 'ipaddress is missing'}
        if hostname in self.hostnames:
            return {'valid': False, 'message': 'duplicate hostname'}
        self.hostnames.append(hostname)
        return {'valid': True, 'message': 'host data is valid'}

    
