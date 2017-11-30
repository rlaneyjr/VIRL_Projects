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

''' Sample usage of function 'connected'.

    Print the function's documentation then invoke the function and print the output.
'''

from __future__ import print_function as _print_function
from basics.inventory import connected, inventory_mounted
from pydoc import render_doc as doc
from pydoc import plain

def main():
    print(plain(doc(connected)))
    device_names = inventory_mounted()
    if not device_names:
        print('There are no devices mounted on the Controller.')
    else:
        device_name = device_names[0]
        print('is connected(%s):' % device_name, connected(device_name))

if __name__ == "__main__":
    main()
