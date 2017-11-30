#!/usr/bin/env python2.7

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

''' Mount a network device that is intentionally unreachable and show that the status is as expected.

    Verify that the device is present in the inventory and is mounted but not connected.
'''

from __future__ import print_function as _print_function
from basics.inventory import inventory, inventory_connected, inventory_mounted, device_mount, device_dismount, mounted
import time

device_name = 'grox'
device_address = '192.168.0.999'
device_port = 830
device_username = 'cisco'
device_password = 'cisco'

def main():
    if mounted(device_name):
        print('Preparation.')     
        print('device_dismount(', device_name, sep='', end=')\n')
        device_dismount(device_name)
        time.sleep(1)
        print()
        
    print('Verify absence of unreachable device.')     
    in_inventory = device_name in inventory()
    in_mounted = device_name in inventory_mounted()
    print(device_name + ' in inventory', in_inventory, sep=': ')
    print(device_name + ' is mounted', in_mounted, sep=': ')
    assert not in_inventory
    assert not in_mounted
    del in_inventory, in_mounted

    print()
    
    print('Discover effect of mounting unreachable device.')     
    print('device_mount(' + device_name, device_address, device_port, sep=', ', end=')\n')
    device_mount(device_name, device_address, device_port, device_username, device_password)
    time.sleep(1)
    in_connected = device_name in inventory_connected()
    in_mounted = device_name in inventory_mounted()
    print(device_name + ' is connected', in_connected, sep=': ')
    print(device_name + ' is mounted', in_mounted, sep=': ')
    assert not in_connected
    assert in_mounted
    
if __name__ == "__main__":
    main()
