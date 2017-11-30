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

''' Sample code to determine ACL capability for a specific device.

    Print the documentation of function 'capability_discovery'.
    Apply the function.
    Print the function output.
    Created on Apr 29, 2015
    @author: mingzhu
'''

from utils.json_compare import  json_compare
from basics.inventory import capability_discovery
from basics.acl import capability_ns, capability_name, acl_delete, acl_list, acl_create_port_grant
from basics.acl import acl_exists
from importlib import import_module
acl_fixture = import_module('learning_lab.05_acl_fixture')


##
##Check device support ACL capability    
##
def is_acl_supported(device_name):
    returnValue = False;
    discovered = capability_discovery(device_name=device_name, capability_name=capability_name, capability_ns=capability_ns)
    if (discovered):
        returnValue = True
    return returnValue


##
##Check ACL is exist on device
##
def is_acl_exist(device_name, acl_name):
    returnValue = False
    if (acl_exists(device_name, acl_name)):
        returnValue  = True
    return returnValue


##
##Get ACL list on device
##
def find_acls_on_device(device_name):
    return acl_list(device_name);


##
## Delete ACLs on device   
##
def delete_acls(acl_list, device_name):
    for acl in acl_list:
        acl_delete(device_name, acl.name)
    

##
##Add ACL to device
##
def add_acl(device_name, acl_name, port, grant, protocol):
    acl_create_port_grant(device_name, acl_name, port, grant, protocol)

##
##Check if we have the acls 
##
def is_same_acl(src_acl, dest_acl):
    flag = json_compare(src_acl, dest_acl)
    return  flag


