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

""" Restore the network to a 'virgin' state.

    Intended usage: the application of any function or sample script is deterministic after restoration.

    Goals:
    * No ACLs applied to interface
    * No ACLs on devices
    * No static routes on devices
    * No interfaces in 'shutdown' state 
    * No devices mounted on the SDN Controller
    
    The goal is achieved by (re)running sample scripts.
    This is 'symmetrical' if the state changes were made by sample scripts.
    Sample scripts are given the opportunity to 'undo' what they may have 'done'.
    
    The output of the scripts is not meaningful and should be ignored because it is
    non-deterministic due to the uncertain network state prior to restoration.
    
    While this script is running there should not be any other interaction 
    with the network devices or SDN Controller. The outcome is undefined if the
    network is modified by anything other than this script.
    
    Out of scope:
    * Any cached state of the SDN Controller, such as Yang models of capabilities
    * Properties and configuration of interfaces except for the up/down state.
    * Unreachable devices
    * Devices not configured in the settings
"""

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

# Context: all devices mounted.
while EX_OK == run_script('01_device_connect'):
    continue

# Context: no interfaces shutdown
while EX_OK == run_script('03_interface_startup'):
    continue

# Context: no ACLs applied to interfaces
while EX_OK == run_script('05_acl_unapply_packet_filter'):
    continue

# Context: no ACLs on devices
while EX_OK == run_script('05_acl_delete'):
    continue

# Context: no static routes on devices
while EX_OK == run_script('04_static_route_delete_all'):
    continue

# Context: all devices unmounted.
run_script('01_inventory_dismount_atomic')
