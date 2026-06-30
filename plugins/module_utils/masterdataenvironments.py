from ansible_collections.alex.cmdb.plugins.module_utils.masterdatacsv import masterdatacsv

class masterdataenvironments:
    def __init__(self, environment):
        environmentinst = masterdatacsv(environment, 'environments.csv')
        self.environmentdata = environmentinst.readall()
