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

''' Sample usage of function 'inventory_summary' to print a HTML table of the inventory with the connected status and number 
    of Netconf capabilities.

    Invoke the function and convert the output to HTML.
    See also: 01_inventory_summary.py
'''

from __future__ import print_function as _print_function

from pydoc import plain
from pydoc import render_doc as doc

from basics.inventory import inventory_summary, InventorySummary


_table_template = '''\
<table>
    <tr>
        <th>Name</th>
        <th>Is Connected</th>
        <th>Number of Capabilities</th>
    </tr>
    %s
</table>
'''

_row_template = '''\
    <tr>
        <td>%s</th>
        <td style="text-align:center">%s</td>
        <td style="text-align:right">%d</td>
    </tr>
'''

def main():
    rows = ''
    for summary in inventory_summary():
        rows += _row_template % summary
    print(_table_template % ''.join(rows))
    
if __name__ == "__main__":
    main()