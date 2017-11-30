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

''' Sample usage of function 'acl_unapply_packet_filter'.

    Print the function's documentation.
    Apply the function to a network device/interface that has an ACL.
'''

from __future__ import print_function as _print_function
from basics.interface import interface_configuration_tuple
from basics.acl_apply import acl_unapply_packet_filter
from basics.acl import inventory_acl
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from pydoc import plain
from pydoc import render_doc as doc

def demonstrate(device_name, interface_name, bound, acl_name):
    '''Un-apply the specified ACL from the specified device/interface/bound.'''
    print('acl_unapply_packet_filter(' + device_name, interface_name, bound, acl_name, sep=', ', end=')\n')
    acl_unapply_packet_filter(device_name, interface_name, bound, acl_name)

def main():
    ''' Select a device and demonstrate.'''
    print(plain(doc(acl_unapply_packet_filter)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        for device_name in inventory:
            for ic in interface_configuration_tuple(device_name):
                print('Consider %s %s in=%s, out=%s' % (device_name, ic.name, ic.packet_filter_inbound, ic.packet_filter_outbound))
                if ic.packet_filter_outbound:
                    demonstrate(device_name, ic.name, 'outbound', ic.packet_filter_outbound)
                    return EX_OK
                if ic.packet_filter_inbound:
                    demonstrate(device_name, ic.name, 'inbound', ic.packet_filter_inbound)
                    return EX_OK
        print('There are no ACLs to unapply. Demonstration cancelled.')
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
