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

"""
Demonstrate how to obtain the properties of network interfaces.

1. for all network interfaces of one network device.
2. for one specific network interface.
"""
from __future__ import print_function
from pydoc import plain
from pydoc import render_doc as doc
from inspect import cleandoc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.render import print_table
from basics.interface import interface_names
from basics.interface_properties import interface_properties
from basics.inventory import inventory_connected

def demonstrate_one(device_name, interface_name):
    """ Obtain, print and return the properties of the specified interface on the specified device."""
    print("Apply function 'interface_properties' to both a network interface and a network device.")
    print('interface_properties(%s, %s)' % (device_name, interface_name))
    properties = interface_properties(device_name, interface_name)
    print_table(properties)
    print()
    return 

def demonstrate_all(device_name):
    """ Obtain, print and return the properties of all network interfaces on the specified device."""
    print("Apply function 'interface_properties' to a network device.")
    print('interface_properties(%s)' % device_name)
    interface_properties_list = interface_properties(device_name)
    print_table(interface_properties_list)
    print()
    return [properties.name for properties in interface_properties_list]

def main():
    """ Select a device/interface and demonstrate."""
    print(cleandoc(__doc__))
    print()
    
    print('Determine which network devices are capable.')
    device_names = inventory_connected()
    print_table(device_names, headers='device-name')
    print()
    for device_name in device_names:
        interface_names = demonstrate_all(device_name)
        if interface_names:
            demonstrate_one(device_name, interface_names[0])
            return EX_OK
    print("There are no suitable network devices and interfaces. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    try:
        sys_exit(main())
    finally:
        print('Function Reference:')
        print(plain(doc(interface_properties)))
        
