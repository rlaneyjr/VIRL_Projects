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
        04_static_route_create
        04_static_route_list
        04_static_route_exists
        04_static_route_json
        04_static_route_delete
        
    To know which devices are static_route capable:
        04_static_route_capability
    
    To browse:
        04_static_route_exists
        04_static_route_list
        04_static_route_json

    To run them all:
        04_static_route_suite (this file)
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


# Run static_route scripts. Context: one static_route capable device.
run_script('01_inventory_dismount_atomic')
while run_script('04_static_route_capability') != EX_OK and run_script('01_device_connect') == EX_OK:
    continue
run_script('04_static_route_capability')
from basics.routes import inventory_static_route
assert inventory_static_route(), "Expect at least one device with static route capability."

# Context: no static routes
while EX_OK == run_script('04_static_route_delete'):
    continue
run_script('04_static_route_exists')
assert run_script('04_static_route_json') != EX_OK
run_script('04_static_route_list')
run_script('04_static_route_delete')

# Context: one static routes
assert run_script('04_static_route_create') == EX_OK
run_script('04_static_route_exists')
assert run_script('04_static_route_json') == EX_OK
run_script('04_static_route_list')
assert run_script('04_static_route_delete') == EX_OK
assert run_script('04_static_route_create') == EX_OK
assert run_script('04_static_route_delete') == EX_OK

# Context: multiple static routes
for i in range(4):
    assert run_script('04_static_route_create') == EX_OK
run_script('04_static_route_exists')
assert run_script('04_static_route_json') == EX_OK
run_script('04_static_route_list')
assert run_script('04_static_route_delete') == EX_OK
