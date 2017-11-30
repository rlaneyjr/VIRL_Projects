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
Demonstrate how to delete static routes.

Introduce function 'static_route_delete'.
Print the function's documentation.

Determine which network devices have 'static route' capability.
Select any one of these network devices.
Select a different network device when no static routes are found.

Apply the function to the selected network device:
- to delete one specific static route.
- to delete all static routes.
"""

from __future__ import print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.render import print_table
from basics.routes import static_route_delete, inventory_static_route, \
    static_route_list

def demonstrate_all(device_name):
    """
    Apply function 'static_route_delete' to all routes on the specified device.
    """
    print()
    print('static_route_delete(%s)' % device_name)
    static_route_delete(device_name)

    print()
    print('static_route_list(%s)' % device_name)
    print_table(static_route_list(device_name), headers='destination-network')


def demonstrate_one(device_name, destination_network):
    """
    Apply function 'static_route_delete' to the specified device and destination.
    """
    print('static_route_delete(%s, %s)' % (device_name, destination_network))
    static_route_delete(device_name, destination_network)
    print()

    print('static_route_list(%s)' % device_name)
    print_table(static_route_list(device_name), headers='destination-network')

def main():
    """ 
    Print the documentation then perform the demonstration(s).
    """
    print(plain(doc(static_route_delete)))

    print('Determine which devices are capable.')
    print('inventory_static_route()')
    inventory = inventory_static_route()
    print_table(inventory, headers='device-name')
    if not inventory:
        print("There are no 'static route' capable devices. Demonstration cancelled.")
    else:
        print()
        for device_name in inventory:
            print('static_route_list(%s)' % device_name)
            route_list = static_route_list(device_name)
            print_table(route_list, headers='destination-network')
            print()
            if route_list:
                demonstrate_one(device_name, route_list[0])
                if len(route_list) > 1:
                    demonstrate_all(device_name)
                return EX_OK
        print("There are no devices with a 'static route' configured. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
