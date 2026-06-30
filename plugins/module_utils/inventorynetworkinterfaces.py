class inventorynetworkinterfaces:
    def __init__(self):
        pass

    def resetvalidation(self):
        pass

    def validatehost(self, hostvars):
        if hostvars.get('prop_networkinterfaces') is None:
            return {'valid': False, 'message': 'networkinterfaces data is empty'}
        networkinterfaces = hostvars['prop_networkinterfaces']
        # if networkinterfaces[0].get('hostname') is None:
        #     return {'valid': False, 'message': 'hostname is missing'}
        # if networkinterfaces[0].get('ipaddress') is None:
        #     return {'valid': False, 'message': 'ipaddress is missing'}
        return {'valid': True, 'message': 'host data is valid'}
