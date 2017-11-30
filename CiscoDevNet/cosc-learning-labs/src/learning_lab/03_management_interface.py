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

''' Sample usage of function 'management_interface' to print the management interfaces for a given mounted device.

    Print the function's documentation.
    Invoke the function.
    Print the function output.
    
    One device that is mounted will be selected for the demonstration.
'''
from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.interface import management_interface
from basics.inventory import inventory_mounted
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL

def demonstrate(device_name):
    ''' Apply function 'management_interface' to the specified device.'''
    print('management_interface(' + device_name, end='): ')
    print(management_interface(device_name))
    
def main():
    ''' Select a device and demonstrate.'''
    print(plain(doc(management_interface)))
    for device_name in inventory_mounted():
        demonstrate(device_name)
        return EX_OK
    print("There are no suitable network devices. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
