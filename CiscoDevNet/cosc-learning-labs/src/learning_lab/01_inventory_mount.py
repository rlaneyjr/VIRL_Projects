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

''' Sample usage of function 'device_mount' to show how to mount Netconf devices.

    Print the function's documentation then apply the function to every device that is configured and not mounted.
'''
from __future__ import print_function as _print_function
from basics.inventory import device_mount, inventory_unmounted, inventory_mounted, inventory
import settings
import time
from pydoc import render_doc as doc
from pydoc import plain

def main():
    print(plain(doc(device_mount)))
    unmounted_list = inventory_unmounted()
    if not unmounted_list:
        print('There are no (configured) devices unmounted.')
    else:
        configured = settings.config['network_device']
        for device_name in unmounted_list:
            device_config = configured[device_name]
            print('device_mount(' + device_name, *device_config.values(), sep=', ', end=')\n')
            device_mount(
                device_name,
                device_config['address'],
                device_config['port'],
                device_config['username'],
                device_config['password'])
#         time.sleep(2) # Allow the Controller time to establish network connections.
                
    # Perform integrity check.     
#     assert set(configured) <= set(inventory_mounted()), 'All configured devices mounted.' 
#     assert set(inventory_mounted()) <= set(inventory()), 'All mounted devices in inventory.'

if __name__ == "__main__":
    main()
    
