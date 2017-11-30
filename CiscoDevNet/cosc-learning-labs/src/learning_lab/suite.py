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
'''

from basics.context import EX_OK
from os.path import basename,splitext
from runpy import run_module

def run_script(script):
    try:
        run_module(script, run_name='__main__')
    except SystemExit as e:
        # Return the exit code of the script.
        # It indicates whether the script able to proceed.         
        # Don't actually exit, though.              
        return e.code

# Run settings scripts.
run_script('00_settings')
run_script('00_devices')
run_script('00_controller')

# Run device scripts. Context: all devices mounted.
run_script('01_inventory_dismount_atomic')
while EX_OK == run_script('01_device_connect'):
    continue
run_script('01_device_mounted')
run_script('01_device_connected')
run_script('01_device_mount')
run_script('01_device_dismount')
run_script('01_device_dismount_unmounted')

# Run device scripts. Context: no devices mounted.
run_script('01_inventory_dismount_atomic')
run_script('01_device_mounted')
run_script('01_device_connected')
run_script('01_device_dismount')
run_script('01_device_dismount_unmounted')
run_script('01_device_mount')

# Run device scripts. Context: one device connected.
run_script('01_inventory_dismount_atomic')
assert EX_OK == run_script('01_device_connect'), "Expected (at least) one connected device, got zero."
run_script('01_device_mounted')
run_script('01_device_connected')
run_script('01_device_dismount')
run_script('01_device_dismount_unmounted')
run_script('01_device_mount')

# Run inventory scripts. Context: all devices mounted.
run_script('01_inventory_dismount_atomic')
while EX_OK == run_script('01_device_connect'):
    continue
run_script('01_inventory')
run_script('01_inventory_mounted')
run_script('01_inventory_unmounted')
# run_script('01_inventory_unreachable')
run_script('01_inventory_connected')
run_script('01_inventory_not_connected')
run_script('01_inventory_integrity')
run_script('01_inventory_summary')
run_script('01_inventory_json')
run_script('01_inventory_mount')

# Run inventory scripts. Context: no devices mounted.
run_script('01_inventory_dismount_atomic')
run_script('01_inventory')
run_script('01_inventory_mounted')
run_script('01_inventory_unmounted')
# run_script('01_inventory_unreachable')
run_script('01_inventory_connected')
run_script('01_inventory_not_connected')
# run_script('01_inventory_integrity')
run_script('01_inventory_summary')
run_script('01_inventory_json')
run_script('01_inventory_mount')

# Run capability scripts. Context: no devices mounted.
run_script('01_inventory_dismount_atomic')
run_script('02_device_capability')
run_script('02_capability_matrix')
run_script('02_capability_discovery')

# Run capability scripts. Context: all devices mounted.
run_script('01_inventory_dismount_atomic')
while EX_OK == run_script('01_device_connect'):
    continue
run_script('02_device_capability')
run_script('02_capability_matrix')
run_script('02_capability_discovery')

run_script('03_interface_suite')

# run_script('04_routes')
run_script('04_topology')
run_script('04_static_route_suite')
run_script('05_story')
      
from basics import render
if render.print_table == render._print_plain_table:
    render.print_table = render._display_rich
    this_script = splitext(basename(__file__))[0]
    run_script(this_script)
