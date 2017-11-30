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

''' Sample usage combining functions 'device_dismount' and 'inventory_connected' to show how to scan for connected devices 
    whilst dismounting devices. Since this happens asynchronously, there is a potential race-condition to monitor for.

    Dismount every device that is mounted and wait for their connections to drop.
    This requires at least one additional HTTP request.
    
    The following scenario is relevant: the Controller has responded successfully to a request to dismount
    a device and a subsequent request of the status responds with 'connected'. This scenario does not occur
    very often. It depends upon the Controller, which might be performing garbage collection. Despite the
    non-deterministic outcome it is evident that the scenario 'can' occur.
'''

from __future__ import print_function as _print_function
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.inventory import device_dismount, inventory_mounted, inventory_connected
from time import sleep

sleep_interval = 0.5

def main():
    mounted_list = inventory_mounted()
    if not mounted_list:
        print('There are no mounted devices to dismount.')
    else:
        for device_name in mounted_list:
            print('device_dismount(' + device_name, end=')\n')
            device_dismount(device_name)
        mounted_list = set(mounted_list)
        sleep_total = 0
        remaining_connected = mounted_list & set(inventory_connected())
        while remaining_connected:
            if sleep_total > sleep_interval * 100:
                print('Time out after %s seconds', sleep_total)
                return 2
            print('Disconnecting', *remaining_connected)
            sleep(sleep_interval)
            sleep_total += sleep_interval
            remaining_connected = mounted_list & set(inventory_connected())
            continue
        print('Dismounted %s device(s), slept for %s seconds' % (len(mounted_list), sleep_total))
        return EX_OK
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
