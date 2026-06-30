from uuid import UUID

class inventorycmdb:
    def __init__(self):
        self.uuids = []

    def resetvalidation(self):
        self.uuids = []

    def validatehost(self, hostvars):
        if hostvars.get('prop_cmdb') is None:
            return {'valid': False, 'message': 'cmdb data is empty'}
        hostcmdb = hostvars['prop_cmdb']
        if hostcmdb.get('uuid') is None:
            return {'valid': False, 'message': 'uuid is missing'}
        try:
            uuid = UUID(hostcmdb['uuid'], version=4)
        except ValueError:
            return {'valid': False, 'message': 'uuid is not valid'}
        if uuid in self.uuids:
            return {'valid': False, 'message': 'duplicate uuid'}
        self.uuids.append(uuid)
        return {'valid': True, 'message': 'host data is valid'}

