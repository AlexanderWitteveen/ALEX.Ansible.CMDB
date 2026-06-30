from ansible.plugins.inventory import BaseInventoryPlugin

DOCUMENTATION = '''
name: secrets
plugin_type: inventory
short_description: My secrets inventory plugin
description:
    - This is my secrets inventory plugin.
options:
    option1:
        description: This is an example option.
        required: True
        type: str
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'secrets'

    def verify_file(self, path):
        valid = super(InventoryModule, self).verify_file(path)
        if valid:
            if path.endswith(('secrets.yml', 'secrets.yaml')):
                return True
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)
        option1 = self.get_option('option1')

        # self.set_options("vault_admin_password", "vault_admin_password1")
        # self.set_options("vault_admin_username", "vault_admin_username1")

        self.inventory.add_group('my_group')
        self.inventory.set_variable('my_group', 'secret', option1)

# https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/data.py
# https://github.com/ansible/ansible/blob/6efb30b43e89e56061311235b3ee97181039a1c9/lib/ansible/plugins/__init__.py#L87