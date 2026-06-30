from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb

class cmdbshellychannels:
    def __init__(self, cmdbinst):
        self.cmdbinst = cmdbinst

    def createindexes(self):
        self.cmdbinst.createindexes("shellychannels", [{ "uuid":1 }, { "id":1 }])
    
    def resetimportdata(self):
        self.keys = []

    def droprecords(self):
        self.cmdbinst.droprecords("shellychannels")

    def importdata(self, hostvars):
        if hostvars.get('prop_shelly') is None or hostvars['prop_shelly'].get('switches') is None:
            return
        for shellyswitch in hostvars['prop_shelly']['switches']:
            key = hostvars['prop_cmdb']['uuid'] + '-' + str(shellyswitch['id'])
            self.keys.append(key)
            shellychannelrecord = {
                'uuid': hostvars['prop_cmdb']['uuid'],
                'name': shellyswitch['name'],
                'id': str(shellyswitch['id']),
                'deviceid': str(hostvars['prop_shelly']['deviceid']),
                'gen': str(hostvars['prop_shelly']['gen']),
            }
            self.cmdbinst.appendrecord("shellychannels", shellychannelrecord)

