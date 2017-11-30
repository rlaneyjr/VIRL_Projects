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

''' Run all sample scripts in a meaningful order.

    The scripts are run in every possible context, such as when no devices are mounted,
    or when a device is mounted and all network interfaces on the data plane are shut-down.
    
    Each script is run the same way as from the command line (or IDE such as Eclipse).
    The goal is to simulate the running of sample scripts in a robotic manner.

    The basic story would be:
        05_acl_create_port_grant
        05_acl_apply_packet_filter
        05_acl_unapply_packet_filter
        05_acl_delete
        
    To know which devices are ACL capable:
        05_acl_capability
    
    To browse:
        05_acl_exists
        05_acl_list
        05_acl_json
        05_acl_json_all
        03_interface_configuration

    To run them all:
        05_story
'''

from basics.context import EX_OK
from runpy import run_module

def run_script(script):
    try:
        run_module(script, run_name='__main__')
    except SystemExit as e:
        # Return the exit code of the script.
        # It indicates whether the script able to proceed.         
        # Don't actually exit, though.              
        return e.code


# Run ACL scripts. Context: one ACL capable device.
run_script('01_inventory_dismount_atomic')
while run_script('05_acl_capability') != EX_OK and run_script('01_device_connect') == EX_OK:
    continue
while EX_OK == run_script('05_acl_delete'):
    continue
from basics.acl import inventory_acl
assert inventory_acl()
run_script('05_acl_capability')
run_script('05_acl_exists')
run_script('05_acl_json')
run_script('05_acl_json_all')
run_script('05_acl_list')
run_script('05_acl_unapply_packet_filter')
run_script('05_acl_apply_packet_filter')
run_script('05_acl_create_port_grant')
run_script('05_acl_exists')
run_script('05_acl_json')
run_script('05_acl_json_all')
run_script('05_acl_list')
run_script('05_acl_unapply_packet_filter')
run_script('05_acl_apply_packet_filter')
run_script('05_acl_unapply_packet_filter')
run_script('05_acl_delete')
