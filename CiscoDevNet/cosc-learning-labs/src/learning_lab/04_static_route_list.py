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
Demonstrate how to list the static routes on a specific network device.

A static route is identified by the destination network. 

Introduce function 'static_route_list'.
Print the function's documentation.

Determine which network devices have 'static route' capability.
Select any one of these network devices.

Apply the function to a selected network device.
Print the function output.
If no routes are found then retry with a different network device.
"""

from __future__ import print_function
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit
from basics.routes import static_route_list, inventory_static_route
from basics.render import print_table

def demonstrate(device_name):
    """
    Apply function 'static_route_list' to the specified device.
    
    Return True when one or more routes are found.
    """
    print('static_route_list(%s)' % device_name)
    routes = static_route_list(device_name)
    print_table(routes, headers='destination-network')
    print()
    return bool(routes)

def main():
    """ 
    Print the function documentation then demonstrate the function usage on a selected device.
     
    Repeat for another device if no 'static route' is configured.
    """
    print(plain(doc(static_route_list)))

    print('Determine which devices are capable.')
    print('inventory_static_route()')
    device_names = inventory_static_route()
    if not device_names:
        print("There are no 'static route' capable devices to examine. Demonstration cancelled.")
    else:
        print_table(device_names, headers='device-name')
        print()
        for device_name in device_names:
            if demonstrate(device_name):
                return EX_OK
        print("There are no devices with a 'static route' configured. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
