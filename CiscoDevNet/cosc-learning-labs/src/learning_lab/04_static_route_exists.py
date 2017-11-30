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
Demonstrate how to determine whether a 'static route' exists on a specific device.
 
Introduce function 'static_route_exists'.
Print the function's documentation.

Generate sample destinations such as 2.2.2.2, 3.3.3.3, etc.
Apply the function to a network device once per sample destination.
Cease when a static route is not found.
"""

from __future__ import print_function
from future.builtins import next
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from pydoc import plain
from pydoc import render_doc as doc
from basics.routes import   static_route_exists, inventory_static_route
from basics.render import print_table
from ipaddress import ip_network

def destination_network_generator():
    counter = 1
    while True:
        counter += 1
        yield ip_network(u"%s.%s.%s.%s/255.255.255.255" % (counter, counter, counter, counter), strict=False) 

def demonstrate(device_name):
    """ 
    Apply function 'static_route_exists' to the specified device for each destination in the list.
    """
    destination_network_iterator = destination_network_generator()
    while True: 
        destination_network = next(destination_network_iterator)
        print('static_route_exists(%s, %s)' % (device_name, destination_network))
        exists = static_route_exists(device_name, destination_network)
        print(exists)
        if not exists:
            return True
        else:
            print()

def main():
    """
    Print the function's documentation then demonstrate the function multiple times on one device.
    """
    print(plain(doc(static_route_exists)))
    
    print('Determine which devices are capable.')
    print('inventory_static_route()')
    device_names = inventory_static_route()
    print_table(device_names, headers='device-name')
    print()

    if not device_names:
        print("There are no 'static route' capable devices to examine. Demonstration cancelled.")
    else:
        for device_name in device_names:
            if demonstrate(device_name):
                return EX_OK
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
