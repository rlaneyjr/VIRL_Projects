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

''' Sample usage of composite of functions 'device_mount' and 'connected'.

    Mount any one device that is configured and not mounted.
    Pause while the Controller connects to the device.
    
    An unreachable device will never connect, so a 'time out' is enforced.
    Repeat the demonstration on a different device if 'time out' occurs.
    
    Exit code is zero when one device is both mounted and connected, otherwise non-zero.
'''

from __future__ import print_function as _print_function

from basics.inventory import device_mount, inventory_unmounted, connected
from settings import config
import time
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL

time_out = 10.0
'''Number of seconds to time out.'''

time_interval = 0.2
'''Initial time interval between checks.'''

def mount_from_settings(device_name):
    """Mount the specified device with the configured settings."""
    device_config = config['network_device'][device_name]
    print('device_mount(' + device_name, *device_config.values(), sep=', ', end=')\n')
    device_mount(
        device_name,
        device_config['address'],
        device_config['port'],
        device_config['username'],
        device_config['password'])

def demonstrate(device_name):
    """ Mount *and* connect the specified device.

        The device must not be mounted already.
        The Controller will attempt connection to the device.
        Return True if connection succeeds before the time-out period elapses.
    """
    mount_from_settings(device_name)
    time_accum = 0.0
    num_checks = 0
    while time_accum < time_out:
        num_checks += 1
        expanding_interval = time_interval * num_checks
        time_accum += expanding_interval  
        # Don't hammer the Controller or it will crash.
        # This not a denial-of-service (DOS) attack ;-)
        time.sleep(expanding_interval)
        print('connected(' + device_name, sep='', end='): ')
        if connected(device_name):
            print(True, 'after %s checks and %s seconds.' % (num_checks, time_accum))
            return True
        else:
            print(False)
            continue
    print('Unconnected after %s checks and %s seconds.' % (num_checks, time_accum))
    return False

def main():
    """Demonstrate on the unmounted devices, stopping when a connection to any device is established."""
    unmounted_list = inventory_unmounted()
    if not unmounted_list:
        print('All configured devices are mounted. Demonstration cancelled.')
    else:
        for device_name in unmounted_list:
            if demonstrate(device_name):
                return EX_OK
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
