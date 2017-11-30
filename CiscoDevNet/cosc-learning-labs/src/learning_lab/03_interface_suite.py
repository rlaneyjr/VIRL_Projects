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

# Run interface scripts. Context: no devices mounted.
run_script('01_inventory_dismount_atomic')
run_script('03_interface_names')
run_script('03_management_interface')
run_script('03_interface_configuration')
run_script('03_interface_configuration_update')
run_script('03_interface_properties')
run_script('03_interface_shutdown')
run_script('03_interface_startup')

# Run interface scripts. Context: all devices mounted.
run_script('01_inventory_dismount_atomic')
while EX_OK == run_script('01_device_connect'):
    continue
run_script('03_interface_names')
run_script('03_management_interface')
run_script('03_interface_configuration')
run_script('03_interface_configuration_update')
run_script('03_interface_properties')
run_script('03_interface_shutdown')
run_script('03_interface_startup')

# Run interface scripts with all devices mounted but all interfaces shutdown.
run_script('01_inventory_dismount_atomic')
while EX_OK == run_script('01_device_connect'):
    continue
while run_script('03_interface_shutdown') == EX_OK:
    continue
try:
    run_script('01_inventory_mount')
    run_script('03_interface_names')
    run_script('03_management_interface')
    run_script('03_interface_configuration')
    run_script('03_interface_configuration_update')
    run_script('03_interface_properties')
finally:
    # Restore all interfaces to 'up'     
    while run_script('03_interface_startup') == EX_OK:
        continue
      
from basics import render
if render.print_table == render._print_plain_table:
    render.print_table = render._display_rich
    this_script = splitext(basename(__file__))[0]
    run_script(this_script)
