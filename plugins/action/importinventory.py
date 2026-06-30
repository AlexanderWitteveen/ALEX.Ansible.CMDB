from ansible.plugins.action import ActionBase
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.template import Templar

from ansible_collections.alex.cmdb.plugins.module_utils.cmdbmongodb import cmdbmongodb
from ansible_collections.alex.cmdb.plugins.module_utils.inventorycmdb import inventorycmdb
from ansible_collections.alex.cmdb.plugins.module_utils.inventoryhost import inventoryhost
from ansible_collections.alex.cmdb.plugins.module_utils.inventorydevice import inventorydevice
from ansible_collections.alex.cmdb.plugins.module_utils.inventorynetworkinterfaces import inventorynetworkinterfaces
from ansible_collections.alex.cmdb.plugins.module_utils.cmdbhosts import cmdbhosts
from ansible_collections.alex.cmdb.plugins.module_utils.cmdbnetworkinterfaces import cmdbnetworkinterfaces
from ansible_collections.alex.cmdb.plugins.module_utils.cmdbshellychannels import cmdbshellychannels

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._display.display('Import Inventory')

        # inventoryengines=[]
        # inventoryengines.append(inventorycmdb())
        # inventoryengines.append(inventoryhost())
        # inventoryengines.append(inventorydevice())
        # inventoryengines.append(inventorynetworkinterfaces())

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

        importengines=[]
        importengines.append(cmdbhosts(cmdbinst))
        importengines.append(cmdbnetworkinterfaces(cmdbinst))
        importengines.append(cmdbshellychannels(cmdbinst))

        for importengine in importengines:
            importengine.resetimportdata()
            importengine.droprecords()
        for host in hosts:
            record = vm.get_vars(host=host)
            for importengine in importengines:
                try:
                    importengine.importdata(record)                    
                except Exception as e:
                    self._display.display('Host: ' + str(host) + ' - ' + str(e))

        result = dict(
            changed=True,
        )
        return result

