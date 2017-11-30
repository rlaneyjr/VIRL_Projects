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

''' Sample usage of function 'inventory_json' to show a list of inventory items in JSON format.

    Demonstrate how to process JSON.
    The function output is 'reduced' to a summary per network device.
    The summary is comparable to function inventory_summary().
    See also: function 'inventory()', which processes XML.
'''

from __future__ import print_function as _print_function
from pydoc import render_doc as doc
from pydoc import plain
from basics.inventory import inventory_json, InventorySummary

name_field = u'id'
connected_field = u'netconf-node-inventory:connected'
capability_field = u'netconf-node-inventory:initial-capability'

def main():
    print(plain(doc(inventory_json)))
    print('Summary of lengthy JSON response:')
    print(*[
        InventorySummary(
            item[name_field],
            connected_field in item and item[connected_field],
            len(item[capability_field]) if capability_field in item else 0
        )
        for item in inventory_json()
    ], sep='\n')
    
if __name__ == "__main__":
    main()
