#!/usr/bin/env python

import json
import sys
import requests

# create the URL from static data plus the args
base = 'http://' + sys.argv[1] + ':8181/restconf/'
topo = 'operational/network-topology:network-topology/topology/pcep-topology'
rpc = 'operations/network-topology-pcep:remove-lsp'
hdr = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}

template = '''
{
    "input": {
        "node": "pcc://%s",
        "name": "%s_to_%s",
        "network-topology-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id=\\"pcep-topology\\"]"
    }
}
'''

# get URL
response = requests.get(base+topo, headers=hdr)

# get data into JSON object
result = json.loads(response.text)

# get the router IDs from the topology
routers = []
for node in result['topology'][0]['node']:
    routers.append(node['network-topology-pcep:path-computation-client']['ip-address'])
    
# sort the list
routers.sort()

# mesh the nodes
for source in routers:
    for dest in routers:
        if (source != dest):
            # nodes are different - so delete the tunnel
            body = template % (source, source, dest)

            response = requests.post(base+rpc, data=body, headers=hdr)

            print source, dest, response
