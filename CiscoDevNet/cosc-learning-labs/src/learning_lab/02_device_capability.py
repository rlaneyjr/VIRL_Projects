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

""" Demonstrate how to discover the capability of one network device.

The following demonstrations are performed:
1. Determine the inventory of network devices and choose one.
2. Discover all capabilities of the chosen network device.
"""

from __future__ import print_function as _print_function
from basics.inventory import  inventory_mounted
from basics.inventory import capability_discovery
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.render import print_table
from pydoc import render_doc as doc, plain
from inspect import cleandoc

def demonstrate(device_name):
    """ Discover, print and return the capabilities of the specified network device."""
    print()
    print("2. Discover all capabilities of the chosen network device.")
    print('capability_discovery(device_name=%s)' % device_name)
    discoveries = capability_discovery(device_name=device_name)
    
    # Discard the outer tuples because they are redundant.     
    capabilities = [discovered.capability for discovered in discoveries]
    capabilities.sort()
    print_table(capabilities)
    return capabilities

def main():
    print(cleandoc(__doc__))
    print()
    print('1. Determine the inventory of network devices and choose one.')
    print('inventory_mounted()')
    device_names = inventory_mounted()
    if not device_names:
        print("There are no mounted network devices. Demonstration cancelled.")
        return EX_TEMPFAIL
    else:
        print_table(device_names, headers='device-name')
    for device_name in inventory_mounted():
        capabilities = demonstrate(device_name)
        if capabilities:
            return EX_OK
    print()
    print("No capabilities were discovered. Demonstration incomplete.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    try:
        sys_exit(main())
    finally:
        print()
        print('Function Reference:')
        print(plain(doc(capability_discovery)))
