from ansible.plugins.action import ActionBase
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.template import Templar

from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._display.display('Clear CMDB')

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

        cmdbinst = cmdbmongodb(environmentid, ipaddress, username, password)
        cmdbinst.clearcmdb()

        cmdbinst.createindexes("environments", [{ "environmentid":1 }, { "environmentname":1 }])
        cmdbinst.createindexes("hosts", [{ "uuid":1 }, { "hostname":1 }])
        cmdbinst.createindexes("networkinterfaces", [{ "uuid":1, "mac":2 }])
        cmdbinst.createindexes("shellychannels", [{ "uuid":1, "id":2 }])

        result = dict(
            changed=True,
        )
        return result

