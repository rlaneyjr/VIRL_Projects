# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function
from basics.inventory import inventory_connected, inventory_mounted
from basics.interface import interface_configuration_tuple, interface_configuration_update, interface_names, InterfaceConfiguration
from unittest.case import TestCase
from unittest import main
from helpers import inventory_purge, inventory_connect

class Test(TestCase):

    def setUp(self):
        """
        Connect every network device configured in the settings.
        """
        inventory_purge()
        inventory_connect()

    def test_interface_configuration_tuple(self):
        device_names = inventory_connected()
        self.assertTrue(device_names, "Expected one or more connected devices.")
        interface_count = 0
        for device_name in device_names:
            for interface_name in interface_names(device_name):
                info = interface_configuration_tuple(device_name, interface_name)
                self.assertEqual(info.name, interface_name)
                self.assertTrue(info.description is None or isinstance(info.description, str))
                self.assertTrue(info.address is None or isinstance(info.address, str))
                self.assertTrue(info.netmask is None or isinstance(info.netmask, str))
                interface_count+=1
        self.assertNotEqual(0, interface_count, 'Expected one or more interfaces.')

    def test_description_absent(self):
        """
        Configure any interface to have no description.
        
        Attempt the task exactly once.
        Restore the original description to the interface.
        """
        for device_name in inventory_connected():
            for interface_name in interface_names(device_name):
                original_info = interface_configuration_tuple(device_name, interface_name)
                interface_configuration_update(device_name, interface_name, None, original_info.address, original_info.netmask, original_info.active, original_info.shutdown)
                modified_info = interface_configuration_tuple(device_name, interface_name)
                self.assertIsNone(modified_info.description)
                interface_configuration_update(device_name, interface_name, original_info.description, original_info.address, original_info.netmask, original_info.active, original_info.shutdown)
                return
        self.fail("Expected (at least) one connected device with (at least) one interface.")

if __name__ == '__main__':
    main()
