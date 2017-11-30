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

''' Sample usage of function 'acl_create_port_grant'.

    Print the function's documentation.
    Apply the function to a network device for each potential ACL.
'''
# devices: ['xrvr-511-53U', 'xrvr-530', 'xrvr-531', 'xrvr-531-i2ss']
# ('Cisco-IOS-XR-ipv4-acl-cfg', ['2013-07-22', None, None, '2015-01-07'])

from __future__ import print_function as _print_function
from importlib import import_module
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.acl import acl_create_port_grant, inventory_acl
acl_fixture = import_module('learning_lab.05_acl_fixture')

def demonstrate(device_name, acl_name, port, grant, protocol):
    ''' Apply function 'acl_create_port_grant' to the specified device and ACL.'''
    print('\nacl_create_port_grant(' + device_name, acl_name, port, grant, protocol, sep=', ', end=')\n')
    acl_create_port_grant(device_name, acl_name, port, grant, protocol)

def main():
    ''' Select a device and demonstrate with each ACL.'''
    print(plain(doc(acl_create_port_grant)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        for device_name in inventory:
            try:
                for acl_sample in acl_fixture.fixtures:
                    demonstrate(device_name, acl_sample.name, acl_sample.port, acl_sample.grant, acl_sample.protocol)
                return EX_OK
            except Exception as e:
                print(e)
                return EX_TEMPFAIL
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
