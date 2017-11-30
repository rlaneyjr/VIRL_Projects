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

''' Sample usage of function 'topology'.

    Print the function's documentation.
    Apply the function to the network.
    Print the function output.
'''

from __future__ import print_function as _print_function
from basics.topology import topology
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_SOFTWARE

def main():
    '''
    This sample script does:
    http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/topology-netconf
    which is not found (404) in ODL Helium.
    It might work in ODL Lithium.
    
    The request for the Yang container *does* succeed:
    http://127.0.0.1:8181/restconf/operational/network-topology:network-topology
    '''
    print(plain(doc(topology)))
    try:
        print(topology("operational"))
        return EX_OK
    except Exception as e:
        print(e)
        return EX_SOFTWARE

if __name__ == "__main__":
    sys_exit(main())

