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

''' Sample usage of function 'interface_configuration_update' to show how to change interface properties.

    Print the function's documentation then invoke the function.
    Use any one interface on any one device that is connected.
    Verify that the configuration has changed.
    Restore the configuration.
'''
from __future__ import print_function as _print_function
from basics.interface import management_interface
from basics.interface import interface_names
from basics.interface import interface_configuration_tuple
from basics.interface import interface_configuration_update
from basics.inventory import inventory_connected
from pydoc import render_doc as doc
from pydoc import plain
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL

# The network interface will temporarily be configured with these settings.
temp_address = '101.101.101.101'
temp_netmask = '255.255.0.0'
temp_description = 'Mutable'

def demonstrate(device_name, interface_name):
    print("Initial configuration:")
    print('interface_configuration_tuple(%s, %s):' % (device_name, interface_name))
    initial = interface_configuration_tuple(device_name, interface_name)
    print(initial)
    
    try:
        print()
        print("Modify configuration:")
        print('interface_configuration_update(%s, %s, %s, %s, %s, %s)' % (device_name, interface_name, temp_description, temp_address, temp_netmask, not initial.shutdown))
        interface_configuration_update(device_name, initial.name, description=temp_description,
                               address=temp_address, netmask=temp_netmask, shutdown=not initial.shutdown)
        print()
        print("Modified configuration:")
        print('interface_configuration_tuple(%s, %s):' % (device_name, interface_name))
        modified = interface_configuration_tuple(device_name, initial.name)
        print(modified)
        assert modified.name == initial.name
        assert modified.description != initial.description
        assert modified.address != initial.address
        assert modified.netmask != initial.netmask
        assert modified.shutdown != initial.shutdown
        
    finally:
        print()
        print("Restore configuration:")
        print('interface_configuration_update(%s, %s, %s, %s, %s, %s)' % (device_name, interface_name, initial.description, initial.address, initial.netmask, initial.shutdown))
        interface_configuration_update(device_name, interface_name, description=initial.description, address=initial.address, netmask=initial.netmask, shutdown=initial.shutdown)
    
        print()
        print("Restored configuration:")
        print('interface_configuration_tuple(%s, %s):' % (device_name, interface_name))
        restored = interface_configuration_tuple(device_name, interface_name)
        print(restored)
        assert restored.name == initial.name
        assert restored.description == initial.description, "Expected '%s' %s got '%s' %s" % (initial.description, type(initial.description), restored.description, type(restored.description))
        assert restored.address == initial.address
        assert restored.netmask == initial.netmask
        assert restored.shutdown == initial.shutdown
        assert restored.active == initial.active

def main():
    print(plain(doc(interface_configuration_update)))
    for device_name in inventory_connected():
        mgmt_name = management_interface(device_name)
        for interface_name in interface_names(device_name):
            # Avoid modifying the management interface.
            if interface_name == mgmt_name:
                continue
            demonstrate(device_name, interface_name)
            return EX_OK
    print("There are no suitable network devices. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
