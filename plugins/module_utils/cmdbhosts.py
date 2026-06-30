from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb

class cmdbhosts:
    def __init__(self, cmdbinst):
        self.cmdbinst = cmdbinst

    def createindexes(self):
        self.cmdbinst.createindexes("hosts", [{ "uuid":1 }, { "hostname":1 }])
    
    def resetimportdata(self):
        self.keys = []

    def droprecords(self):
        self.cmdbinst.droprecords("hosts")

    def importdata(self, hostvars):
        self.keys.append(hostvars['prop_cmdb']['uuid'])
        hostrecord = {
            'uuid': hostvars['prop_cmdb']['uuid'],
            'hostname': hostvars['prop_host']['hostname'],
            'ipaddress': hostvars['prop_host']['ipaddress']
        }
        self.cmdbinst.appendrecord("hosts", hostrecord)


