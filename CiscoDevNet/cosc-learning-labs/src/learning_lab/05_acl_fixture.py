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

''' Data shared by ACL sample scripts.'''

from collections import namedtuple

AclPortGrantProtocol = namedtuple('AclPortGrantProtocol', ['name', 'port', 'grant', 'protocol'])
    
fixtures = [
    AclPortGrantProtocol(name='port_echo_deny_udp', grant='deny', port='echo', protocol='udp'),
    AclPortGrantProtocol(name='port_echo_permit_udp', grant='permit', port='echo', protocol='udp'),
    AclPortGrantProtocol(name='port_www_deny_tcp', grant='deny', port='www', protocol='tcp'),
    AclPortGrantProtocol(name='port_www_permit_tcp', grant='permit', port='www', protocol='tcp')
]
