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

""" Demonstrate how to discover the capability of network devices.

The following demonstrations are performed:
1. Discover all capabilities of all network devices.
2. Discover which network devices are capable of a specific task.
3. Attempt discovery of a capability that is unavailable.
"""

from __future__ import print_function as _print_function
from basics.inventory import  capability_discovery
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.render import print_table
from pydoc import render_doc as doc, plain
from inspect import cleandoc

def demonstrate_all():
    print()
    print('1. Discover all capabilities of all network devices.')
    print('Display summaries because the entire list is too long.')
    print('capability_discovery()')
    discoveries = capability_discovery()
    capabilities = set(discovered.capability for discovered in discoveries)
    device_names = set([discovered.device_name for discovered in discoveries])

    capability_by_device = lambda device_name: [discovered.capability for discovered in discoveries if discovered.device_name == device_name]
    device_by_capability_name = lambda capability_name: set([discovered.device_name for discovered in discoveries if discovered.capability.name == capability_name])
    capability_revision_by_name = lambda capability_name: set([capability.revision for capability in capabilities if capability.name == capability_name])
    capability_name_by_revision = lambda capability_revision: set([capability.name for capability in capabilities if capability.revision == capability_revision])
    capability_namespace_by_name = lambda capability_name: set([capability.namespace for capability in capabilities if capability.name == capability_name])
    capability_name_by_namespace = lambda capability_namespace: set([capability.name for capability in capabilities if capability.namespace == capability_namespace])
    capability_revision_by_namespace = lambda capability_namespace: set([capability.revision for capability in capabilities if capability.namespace == capability_namespace])
    
    summary = [(device_name, len(capability_by_device(device_name))) for device_name in device_names]
    summary.sort()
    print()
    print_table(summary, headers=('device name', '# capabilities'))
    
    capability_names = set([capability.name for capability in capabilities])
    summary = [(
            capability_name, 
            len(device_by_capability_name(capability_name)), 
            len(capability_revision_by_name(capability_name)),
            len(capability_namespace_by_name(capability_name))
        ) for capability_name in capability_names]
    summary.sort()
    print()
    print_table(summary, headers=('capability name', '# devices', '# revisions', '# name-spaces'))

    print()
    print('The following summaries consider each capability only once, ')
    print('regardless of how many network devices have that capability.')

    capability_revisions = set([capability.revision for capability in capabilities])
    summary = [(revision, len(capability_name_by_revision(revision))) for revision in capability_revisions]
    summary.sort()
    print()
    print('Display revisions of capabilities in sorted order (often chronological).')
    print_table(summary, headers=('capability revision', '# capabilities'))

    capability_namespaces = set([capability.namespace for capability in capabilities])
    summary = [(
            namespace, 
            len(capability_name_by_namespace(namespace)),
            len(capability_revision_by_namespace(namespace))
        ) for namespace in capability_namespaces]
    summary.sort()
    print()
    print('Display name-spaces of capabilities in sorted order.')
    print()
    print_table(summary, headers=('capability name-space', '# capabilities', '# revisions'))

    print()
    print('Note that all the information contained in the multiple summaries, above, \nwas obtained with a single HTTP request (RPC) to the Controller.')
    return discoveries
    
def demonstrate_by_capability(capability_name, capability_namespace):
    print()
    print('2. Discover which network devices are capable of a specific task.')
    print('For each task that will be performed by an application, the appropriate \ncapability must be determined.')
    print('For convenience, this demonstration chooses any one capability \nand searches for devices that are capable.')
    print()
    print('capability_discovery(%s, %s)' % (capability_name, capability_namespace))
    discoveries = capability_discovery(capability_name, capability_namespace)
    print_table([(discovered.device_name, discovered.capability.revision) for discovered in discoveries], 
                headers=('device-name', 'capability-revision'))
    
def demonstrate_not_found():
    print()
    print('3. Attempt discovery of a capability that is unavailable.')
    print('If there are no capable devices then an empty list is returned.')
    print('This is demonstrated using a capability that is known to be unavailable.')
    print()
    capability_name = 'teleport'
    capability_namespace = 'http://startrek.com/ns/yang/'
    print('capability_discovery(%s, %s)' % (capability_name, capability_namespace))
    discoveries = capability_discovery(capability_name, capability_namespace)
    print_table([(discovered.device_name, discovered.capability.revision) for discovered in discoveries], 
                headers=('device-name', 'capability-revision'))
    
def main():
    print(cleandoc(__doc__))
    discoveries = demonstrate_all()
    if discoveries:
        discovered = discoveries[0]
        demonstrate_by_capability(
            discovered.capability.name, 
            discovered.capability.namespace)
        demonstrate_not_found()
        return EX_OK
    else:
        demonstrate_not_found()
        print()
        print("There are no capable network devices. Demonstration incomplete.")
        return EX_TEMPFAIL

if __name__ == "__main__":
    try:
        sys_exit(main())
    finally:
        print()
        print('Function Reference:')
        print(plain(doc(capability_discovery)))
