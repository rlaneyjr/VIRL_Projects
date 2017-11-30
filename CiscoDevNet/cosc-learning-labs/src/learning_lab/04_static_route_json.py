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
Demonstrate how to obtain and navigate static routes in JSON representation.

Introduce function 'static_route_json'.
Print the function's documentation.

Determine which network devices have 'static route' capability.
Select any one of these network devices.
Select a different network device when no static routes are found.

Apply the function to the selected network device:
- to obtain all static routes.
- to obtain one specific static route.

Demonstrate the navigation of the 'static route' data structure.
Print the JSON representation of one static route.
"""

from __future__ import print_function
from collections import OrderedDict
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import EX_OK, EX_TEMPFAIL
from ipaddress import ip_network
from basics.render import print_table
from basics.context import sys_exit
from basics.routes import static_route_json, inventory_static_route
import json

def demonstrate_all(device_name):
    """
    Apply function 'static_route_json' to the specified device without 
    specifying a static route destination.

    Return a list of static route destination networks (may be empty).
    """
    print('Request all static routes.')
    print('static_route_json(%s)' % device_name)
    route_list = static_route_json(device_name)
    if not route_list:
        print(None)
        print()
        return []
    
    print_table([OrderedDict([
            ("device", device_name),
            ("destination", "%s/%s" % (route['prefix'], route['prefix-length'])),
            ("next-hop", next_hop_address(route))
        ]) for route in route_list
    ])
    print()
    return [ip_network("%s/%s" % (route['prefix'], route['prefix-length'])) for route in route_list]

def next_hop_address(route):
    try:
        return route['vrf-route']['vrf-next-hops']['next-hop-address'][0]['next-hop-address']
    except KeyError as ke:
        return route

def demonstrate_one(device_name, destination_network):
    """
    Apply function 'static_route_json' to the specified device and destination.

    Return True if the static route is found.
    """
    print('Request a specific static route.')
    print('static_route_json(%s, %s)' % (device_name, destination_network))
    route = static_route_json(device_name, destination_network)
    print(json.dumps(route, indent=2, sort_keys=True))
    return True

def main():
    """ 
    Print the documentation then perform the demonstration(s).
    """
    print(plain(doc(static_route_json)))

    print('Determine which devices are capable.')
    print('inventory_static_route()')
    inventory = inventory_static_route()
    if not inventory:
        print(None)
        print("There are no 'static route' capable devices. Demonstration cancelled.")
    else:
        print_table(inventory)
        print()
        for device_name in inventory:
            route_list = demonstrate_all(device_name)
            if route_list:
                return EX_OK if demonstrate_one(device_name, route_list[0]) else EX_TEMPFAIL
            else:
                print()
        print("There are no devices with a 'static route' configured. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
