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

''' Sample usage of function 'acl_json_all'.

    Print the function's documentation.
    Apply the function to a network device.
    Print the function output.
    If no ACLs found then retry with a different network device.
'''

from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.acl import acl_json_all, inventory_acl
import json

def demonstrate(device_name):
    ''' Apply function 'acl_json_all' to the specified device.'''
    print('acl_json_all(' + device_name, sep=', ', end=')\n')
    acl_list = acl_json_all(device_name)
    if acl_list:
        for acl in acl_list:
            print(json.dumps(acl, sort_keys=False, indent=2, separators=(',', ': ')))
    else:
        print('\t', acl_list)
    return len(acl_list) != 0

def main():
    ''' Select a device and demonstrate, repeat until one ACL found.'''
    print(plain(doc(acl_json_all)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        for device_name in inventory:
            if demonstrate(device_name):
                return EX_OK
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
