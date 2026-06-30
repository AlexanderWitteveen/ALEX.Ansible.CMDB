from ansible.plugins.inventory import BaseInventoryPlugin

DOCUMENTATION = '''
name: cmdb
plugin_type: inventory
short_description: My cmdb inventory plugin
description:
    - This is my cmdb inventory plugin.
options:
    option1:
        description: This is an example option.
        required: True
        type: str
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'cmdb'

    def verify_file(self, path):
        valid = super(InventoryModule, self).verify_file(path)
        if valid:
            if path.endswith(('cmdb.yml', 'cmdb.yaml')):
                return True
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)
        option1 = self.get_option('option1')
        # admin_username = self.get_option('vault_admin_username')
        # admin_password = self.get_option('vault_admin_password')

        self.inventory.add_group('my_group')
        self.inventory.set_variable('my_group', 'web', option1)
        # self.inventory.set_variable('my_group','admin_username', admin_username)
        # self.inventory.set_variable('my_group','admin_password', admin_password)

        self.inventory.add_host('host1', group='my_group')
        self.inventory.add_host('host2', group='my_group')
        self.inventory.add_host('host3')
        self.inventory.set_variable('host1', 'ansible_host', '192.168.1.10')
        self.inventory.set_variable('host2', 'ansible_host', '192.168.1.11')
        self.inventory.set_variable('host3', 'ansible_host', '192.168.1.12')
