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
from basics.inventory import device_control, inventory_mounted, mounted, device_dismount, inventory_unmounted
from helpers import mount_from_settings
from unittest.case import TestCase
from unittest import main

class Test(TestCase):

    def setUp(self):
        mounted_list = inventory_mounted()
        if mounted_list:
            for device_name in mounted_list:
                device_dismount(device_name)
                self.assertFalse(mounted(device_name), 'Expected dismount: ' + device_name)

    def test_device_mount(self):
        device_names = inventory_unmounted()
        self.assertTrue(device_names, 'One or more devices must be configured.')
        for device_name in device_names:
            expected = mount_from_settings(device_name)
            self.assertTrue(mounted(device_name), 'Expected mounted: ' + device_name)
            actual = device_control(device_name)
            self.assertEqual(device_name, actual.device_name)
            self.assertEqual(expected.device_name, actual.device_name)
            self.assertEqual(expected.address, actual.address)
            self.assertEqual(expected.port, actual.port)
            self.assertEqual(expected.username, actual.username)
            self.assertEqual(expected.password, actual.password)
                            
if __name__ == '__main__':
    main()
