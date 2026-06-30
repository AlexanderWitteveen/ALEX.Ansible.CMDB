from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb

class cmdbenvironments:
    def __init__(self, cmdbinst):
        self.cmdbinst = cmdbinst

    def createindexes(self):
        self.cmdbinst.createindexes("environments", [{ "environmentid":1 }, { "environmentname":1 }])
    
    def mergedata(self, allnewrecords):
        self.cmdbinst.mergedata("environments", "environmentid", allnewrecords)

