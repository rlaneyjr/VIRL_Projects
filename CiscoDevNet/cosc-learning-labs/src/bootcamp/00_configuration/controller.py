#!/usr/bin/env python3.4

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

''' Connect to the Controller.

    Establish a connection to the Controller and display relevant information.
'''

from __future__ import print_function
import settings
import socket

def main():
    # Controller end-point
    controller = settings.config['odl_server']

    # Socket
    s = socket.socket()
    
    # Connect
    try:
        s.connect((controller['address'], controller['port']))
        print('client', s.getsockname(), '-->', 'controller', s.getpeername())
    except Exception as e:
        print('client -->', controller['address'], controller['port'], e)
    finally:
        s.close()
        del s

if __name__ == "__main__":
    main()
