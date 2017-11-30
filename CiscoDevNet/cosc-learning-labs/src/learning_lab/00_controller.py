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

''' 
    Connects to the controller and authenticates, as a basic sanity check that the controller is reachable and responding to requests.
'''

from __future__ import print_function as _print_function
import settings 
from basics.odl_http import coordinates as odl_coordinates, odl_http_head
from sys import stderr
from basics.context import sys_exit, EX_OK, EX_CONFIG
from basics.render import print_table

if __name__ == "__main__":
    # It is essential to import module 'settings' because it injects the
    # Controller settings into attribute 'odl_http.coordinates'.     
    # The code below references module 'settings' to prevent it from
    # being auto-removed due to an 'unused import' warning.
    if not settings:
        print('Settings must be configured', file=stderr)
    
    print_table(odl_coordinates)
    print()
    
    try:
        print('Connecting...')
        response = odl_http_head(
            # Use any URL that is likely to succeed.                                   
            url_suffix='operational/opendaylight-inventory:nodes',
            accept='application/json',
            expected_status_code=[200, 404, 503])
        outcome = {
            "status code":response.status_code,
            "status":
                'Not found (either the URL is incorrect or the controller is starting).'
                if response.status_code == 404 else
                'Service unavailable (allow 5 or 10 minutes for controller to become ready)'
                if response.status_code == 503 else
                'OK'
                if response.status_code == 200 else
                'Unknown',
            "method":response.request.method,
            "url":response.url}
        print_table(outcome)
        exit_code = EX_OK
    except Exception as e:
        exit_code = EX_CONFIG
        print(e, file=stderr)
    finally:
        sys_exit(exit_code)

