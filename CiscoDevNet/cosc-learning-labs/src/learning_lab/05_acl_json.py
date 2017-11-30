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

''' Sample usage of function 'acl_json'.

    Print the function's documentation.
    Apply the function to a network device and ACL.
    Print the function output.
    If no ACL found then retry with a different network device.
'''

from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.acl import acl_json, inventory_acl
import json
from importlib import import_module
acl_fixture = import_module('learning_lab.05_acl_fixture')

def demonstrate(device_name, acl_name):
    ''' Apply function 'acl_json' to the specified device.'''
    print('\nacl_json(' + device_name, acl_name, sep=', ', end=')\n')
    acl = acl_json(device_name, acl_name)
    if acl:
        print(json.dumps(acl, indent=2))
    else:
        print('\t', acl)
    return acl is not None

def main():
    ''' Select a device and demonstrate, repeat until one ACL found.'''
    print(plain(doc(acl_json)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        for device_name in inventory:
            for acl_sample in acl_fixture.fixtures:
                if demonstrate(device_name, acl_sample.name):
                    return EX_OK
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
