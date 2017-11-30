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
Display a matrix of capabilities and network devices.

The matrix has a row for each capability discovered on the network.
The matrix has a column for each network device.
Where each row and column intersect, the presence of that capability, on that 
device, is indicated by the appearance of the revision (of the capability) or 
blank if incapable.

When the network contains identical devices, the columns of the matrix are 
identical (and therefore redundant). This is often the case in a demonstration.
However, when different models and products of network devices are combined, 
the matrix is a rich source of information. It provides a convenient and concise
summary of a heterogeneous network.

All the information in the matrix is obtained from a single (HTTP) request to 
the Controller.
"""

from __future__ import print_function as _print_function
from basics.inventory import capability_discovery
from itertools import chain
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.render import print_table
from pydoc import render_doc as doc, plain
from inspect import cleandoc

def demonstrate(discoveries):
    # Structure of map is {capability-id : revision-by-device}
    # where capability-id is (capability-name, capability-namespace)
    # and revision-by-device is {device-name : capability-revision}.   
    revision_by_capability = {}
    device_names = set()
    
    # Visit each discovery once and collect the capability identifier as a key
    # and the capability revision as a (nested) value.
    # During this single pass of discoveries, collect device names too.
    for discovered in discoveries:
        capability_id = (discovered.capability.name, discovered.capability.namespace)
        revision_by_device = revision_by_capability.get(capability_id, {})
        if not revision_by_device:
            revision_by_capability[capability_id] = revision_by_device
        revision_by_device[discovered.device_name] = discovered.capability.revision
        device_names.add(discovered.device_name)
        
    # Order the devices alphabetically by name.
    # This makes the column order deterministic.              
    device_names = sorted(device_names)

    # Flatten the dict into a 2D table.     
    # Structure of table is [row, ...]
    # where row is (capability-name, capability-namespace, revision, ...)
    # where revision, ... is ordered list of one revision per device.               
    table = [
        tuple(chain(capability_id, [revision_by_device.get(device_name, '') for device_name in device_names]))             
        for (capability_id, revision_by_device) in revision_by_capability.items()
    ]
    
    # Order the table by capability name.     
    # This makes the row order deterministic.              
    table.sort()
    headers = tuple(chain(('capability-name', 'capability-namespace'), device_names))
    print_table(table, headers=headers)

def main():
    print(cleandoc(__doc__))
    print()
    print('capability_discovery()')
    discoveries = capability_discovery()
    if not discoveries:
        print("There are no capable network devices. Demonstration cancelled.")
        return EX_TEMPFAIL
    demonstrate(discoveries)
    return EX_OK

if __name__ == "__main__":
    try:
        sys_exit(main())
    finally:
        print()
        print('Function Reference:')
        print(plain(doc(capability_discovery)))
        