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
from basics.interface import interface_names
from unittest.case import TestCase
from basics.inventory import inventory_connected
from unittest import main
from helpers import inventory_connect, inventory_purge

class Test(TestCase):

    def setUp(self):
        """
        Connect every network device configured in the settings.
        """
        inventory_purge()
        inventory_connect()
        

    def test_interface_names(self):
        device_names = inventory_connected()
        self.assertTrue(device_names, "Expected one or more connected devices.")
        for device_name in device_names:
            interfaces = interface_names(device_name)
            self.assertGreater(len(interfaces), 1, 'Expected multiple interfaces, got %d' % len(interfaces))

if __name__ == '__main__':
    main()
