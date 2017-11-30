#!/usr/bin/env python2.7

# Copyright 2014 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

''' Sample usage of function 'interface_names' to print the interface names for a given device.

    Print the function's documentation then apply the function to any one device that is mounted and connected.
'''

from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.interface import interface_names
from basics.inventory import inventory_connected, inventory_mounted

def demonstrate(device_name):
    ''' Apply function 'interface_names' to the specified device.'''
    print('interface_names(' + device_name, end=')\n')
    print(interface_names(device_name))

def main():
    ''' Select a device and demonstrate.'''
    print(plain(doc(interface_names)))
    mounted_list = inventory_mounted()
    connected_list = inventory_connected()
    device_list = list(set(connected_list) & set(mounted_list))
    for device_name in device_list:
        return demonstrate(device_name)
    print('There are no mounted, connected devices to examine. Demonstration cancelled.')

if __name__ == "__main__":
    main()
