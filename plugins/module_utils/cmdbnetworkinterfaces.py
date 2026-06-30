from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb

class cmdbnetworkinterfaces:
    def __init__(self, cmdbinst):
        self.cmdbinst = cmdbinst

    def createindexes(self):
        self.cmdbinst.createindexes("networkinterfaces", [{ "uuid":1 }, { "mac":1 }])
    
    def resetimportdata(self):
        self.keys = []

    def droprecords(self):
        self.cmdbinst.droprecords("networkinterfaces")

    def importdata(self, hostvars):
        for networkinterface in hostvars['prop_networkinterfaces']:
            key = hostvars['prop_cmdb']['uuid'] + '-' + networkinterface['mac']
            self.keys.append(key)
            networkinterfacerecord = {
                'uuid': hostvars['prop_cmdb']['uuid'],
                'hostname': hostvars['prop_host']['hostname'],
                'name': networkinterface['name'],
                'ipaddress': networkinterface['ipaddress'],
                'mac': networkinterface['mac'],
            }
            self.cmdbinst.appendrecord("networkinterfaces", networkinterfacerecord)
