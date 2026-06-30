from ansible.plugins.action import ActionBase
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.template import Templar

from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb
from ansible_collections.alex.cmdb.plugins.module_utils.cmdbenvironments import cmdbenvironments
# from ansible_collections.alex.cmdb.plugins.module_utils.masterdatacsv import masterdatacsv
from ansible_collections.alex.cmdb.plugins.module_utils.masterdataenvironments import masterdataenvironments

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._display.display('Import Master Data')

        dl = DataLoader()
        im = InventoryManager(loader=dl, sources=task_vars['ansible_inventory_sources'])
        vm = VariableManager(loader=dl, inventory=im)
        hosts=im.get_hosts()
        host=list(filter(lambda h: h.name == task_vars['ansible_host'], hosts))[0]
        vars = vm.get_vars(host=host)
        tm = Templar(loader=dl, variables=vars)

        environmentid = tm.template(task_vars['prop_cmdb']['environment'])
        ipaddress = tm.template(task_vars['prop_host']['ipaddress'])
        username = tm.template(task_vars['prop_admin_username'])
        password = tm.template(task_vars['prop_admin_password'])

        environmentinst = masterdataenvironments(environmentid)
        environmentdata = environmentinst.environmentdata

        cmdbinst = cmdbmongodb(environmentid, ipaddress, username, password)
        cmdbenvironmentinst = cmdbenvironments(cmdbinst)
        cmdbenvironmentinst.createindexes()

        cmdbinst.droprecords("environments")
        for environmentrecord in environmentdata:
            cmdbinst.appendrecord("environments", environmentrecord)

        result = dict(
            changed=True,
        )
        return result
