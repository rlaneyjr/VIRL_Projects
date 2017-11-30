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

''' Sample usage of function 'device_mount' to mount a device in the configuration.

    Print the function's documentation then apply the function to any one device that is configured and not mounted.
'''

from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.inventory import device_mount, inventory_unmounted
from settings import config


def demonstrate(device_name):
    device_config = config['network_device'][device_name]
    print('device_mount(' + device_name, *device_config.values(), sep=', ', end=')\n')
    device_mount(
        device_name,
        device_config['address'],
        device_config['port'],
        device_config['username'],
        device_config['password'])

def main():
    print(plain(doc(device_mount)))
    for device_name in inventory_unmounted():
        demonstrate(device_name)
        return EX_OK
    print('All configured devices are mounted. Demonstration cancelled.')
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
