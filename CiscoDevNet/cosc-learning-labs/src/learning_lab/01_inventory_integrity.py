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

''' Integrity check of all inventory related function output.

    Obtain the entire inventory and the various subsets and validate them.
'''

from __future__ import print_function as _print_function
from basics.inventory import inventory_not_connected, inventory, inventory_connected, inventory_mounted, inventory_unmounted

def main():
    inventory_set = set(inventory())
    inventory_connected_set = set(inventory_connected())
    inventory_not_connected_set = set(inventory_not_connected())
    inventory_mounted_set = set(inventory_mounted())
    inventory_unmounted_set = set(inventory_unmounted())
    empty_set = set()
    
    print("The set of 'connected' devices is a subset of the inventory:",
           inventory_connected_set <= inventory_set)
    assert inventory_connected_set <= inventory_set
    
    print("The set of 'not connected' devices is also a subset of the inventory:",
           inventory_not_connected_set <= inventory_set)
    assert inventory_not_connected_set <= inventory_set
    
    print("There are no network devices in both the 'connected' set and the 'not connected' set:",
           inventory_not_connected_set & inventory_connected_set == empty_set)
    assert inventory_not_connected_set & inventory_connected_set == empty_set
    
    print("Every network device in the inventory is in either the 'connected' set or the 'not connected' set:",
           inventory_connected_set | inventory_not_connected_set == inventory_set)
    assert inventory_connected_set | inventory_not_connected_set == inventory_set
    
    print()
    
    print("The set of 'mounted' devices is a subset of the inventory:",
           inventory_mounted_set <= inventory_set)
    assert inventory_mounted_set <= inventory_set
    
    print("The set of 'unmounted' devices has no intersection with the inventory:",
           inventory_unmounted_set & inventory_set == empty_set)
    assert inventory_unmounted_set & inventory_set == empty_set, 'Expect no intersection, got %s' % (inventory_unmounted_set & inventory_set)
    
    print("There are no network devices in both the 'mounted' set and the 'unmounted' set:",
           inventory_unmounted_set & inventory_mounted_set == empty_set)
    assert inventory_unmounted_set & inventory_mounted_set == empty_set
    
if __name__ == "__main__":
    main()
