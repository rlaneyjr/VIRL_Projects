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

''' Sample usage of function 'device_dismount' to show how to dismount a given device.

    Print the function's documentation then apply the function to any one device that is mounted.
'''

from __future__ import print_function as _print_function
from basics.inventory import device_dismount, inventory_mounted
from pydoc import render_doc as doc
from pydoc import plain
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL

def demonstrate(device_name):
    print('device_dismount(' + device_name, end=')\n')
    device_dismount(device_name)

def main():
    print(plain(doc(device_dismount)))
    for device_name in inventory_mounted():
        demonstrate(device_name)
        return EX_OK
    print('There are no mounted devices to dismount. Demonstration cancelled.')
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
