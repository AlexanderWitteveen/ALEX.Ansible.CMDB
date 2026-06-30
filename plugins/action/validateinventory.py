from ansible.plugins.action import ActionBase
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.template import Templar

from ansible_collections.alex.cmdb.plugins.module_utils.inventorycmdb import inventorycmdb
from ansible_collections.alex.cmdb.plugins.module_utils.inventoryhost import inventoryhost
from ansible_collections.alex.cmdb.plugins.module_utils.inventorydevice import inventorydevice
from ansible_collections.alex.cmdb.plugins.module_utils.inventorynetworkinterfaces import inventorynetworkinterfaces

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._display.display('Validate Inventory')

        engines=[]
        engines.append(inventorycmdb())
        engines.append(inventoryhost())
        engines.append(inventorydevice())
        engines.append(inventorynetworkinterfaces())

        for engine in engines:
            engine.resetvalidation()

        dl = DataLoader()
        im = InventoryManager(loader=dl, sources=task_vars['ansible_inventory_sources'])
        vm = VariableManager(loader=dl, inventory=im)
        tm = Templar(loader=dl, variables=vm.get_vars())

        hosts=im.get_hosts()
        self._display.display('Hosts: %s' % (len(hosts)))
        countvalid = 0
        for host in hosts:
            message = 'Host: %s' % (host)
            hostvars = vm.get_vars(host=host)
            isvalid=True
            for engine in engines:
                result = engine.validatehost(hostvars)
                if not result['valid']:
                    # message += ": " + result['message']
                    # display = self._display.display(message)
                    self._display.display('Host: ' + str(host) + ' - ' + result['message'])
                    isvalid = False
                    break
            if isvalid:
                countvalid += 1

        result = dict(
            changed=False,
            valid_hosts=countvalid,
            total_hosts=len(hosts)
        )
        return result


