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
Demonstrate how to discover network devices that have 'static route' capabilities.

If there are no such devices then all sample scripts prefixed with 
`05_static_route_` are unable to perform their demonstrations.
"""

from __future__ import print_function
from pydoc import render_doc as doc, plain
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.routes import capability_ns, capability_name
from basics.inventory import capability_discovery
from basics.render import print_table
from inspect import cleandoc

def demonstrate():
    ''' Apply function 'capability_discovery' to the specified device for required capability. '''
    print('capability_discovery(capability_name=%s, capability_ns=%s)' % (capability_name, capability_ns))
    discoveries = capability_discovery(capability_name=capability_name, capability_ns=capability_ns)
    print_table([(
            discovered.device_name, 
            discovered.capability.revision
        ) for discovered in discoveries], headers=(
            'device-name',
            'revision'
        ))
    return discoveries

def main():
    ''' Document and demonstrate the function until a capable device is found.'''
    print(cleandoc(__doc__))
    print()
    discoveries = demonstrate()
    if not discoveries:
        print()
        print("There are no 'static route' capable network devices. Demonstration insufficient.")
        return EX_TEMPFAIL
    return EX_OK

if __name__ == "__main__":
    try:
        sys_exit(main())
    finally:
        print()
        print('Function Reference:')
        print(plain(doc(capability_discovery)))
