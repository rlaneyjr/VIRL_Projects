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

''' Connect to each configured Network Device and display the details of the local socket, from which you are connecting, 
    and the remote socket to which you are connecting on the device. This helps establish whether the configured Network 
    Devices are reachable. Note that it is perfectly possible that the Network Devices are NOT reachable from where this 
    script would be run, but that the controller is, and that the controller can see the Network Devices.
'''

from __future__ import print_function as _print_function
import settings
import socket

if __name__ == "__main__":
    for (device_name, device_config) in settings.config['network_device'].items():
        device_address = device_config['address']
        device_port = device_config['port']
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((device_address, device_port))
            print(device_name, s.getsockname(), '-->', s.getpeername())
        except Exception as e:
            print(device_name, '-->', device_address, device_port, e)
        finally:
            s.close()
            del s
