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

''' Sample usage of function 'device_dismount(device_name)' on an unmounted device, that is not configured, 
    to test that there is an expected exception.

    Dismount a device that is not mounted.
    The outcome is undefined.
    This script reports whether or not an exception is thrown.
    
    The function 'device_dismount' does not check if the device is mounted.
    Library function 'mounted(device_name)' is relevant but not reliable.
    The unreliability is due to the possibility of concurrent activity.
'''

from __future__ import print_function as _print_function
from basics.inventory import device_dismount, mounted
from pydoc import render_doc as doc
from pydoc import plain

device_name = 'dark'

def main():
    print(plain(doc(device_dismount)))
    assert not mounted(device_name)
    try:
        print('device_dismount(' + device_name, end=')\n')
        device_dismount(device_name)
        exception = False
        print('no exception')
    except Exception:
        exception = True
    finally:
        print('exception:', exception)
        assert not mounted(device_name)

if __name__ == "__main__":
    main()
