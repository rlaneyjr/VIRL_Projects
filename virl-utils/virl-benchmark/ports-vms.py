#!/usr/bin/env python
#
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# Show all ports of all VM instances for
# all users and topologies.
# Like the console port and the VNC port
#
# rschmied@cisco.com
#
# modified by sebastian.rieger@informatik.hs-fulda.de to display telnet console ports of running nodes in a topology
#


import os, libvirt, re, sys
from keystoneclient import client as keystone
from novaclient import client as nova
from xml.dom.minidom import parseString

"""

In [14]: m.group(0)
Out[14]: '</guest/endpoint>-<Sample_Project@asa-test-topo-yJHnoK>-<iosv-2>-<Multipoint Connection-1>'

In [15]: m.group(1)
Out[15]: '/guest/endpoint'

In [16]: m.group(2)
Out[16]: 'Sample_Project'

In [16]: m.group(3)
Out[16]: 'asa-test-topo'

In [17]: m.group(4)
Out[17]: 'iosv-2'

In [18]: m.group(5)
Out[18]: 'Multipoint Connection-1'

will not match jumphost ports!
not interested in these, anyway

"""

class KeystoneV3NovaAuthPlugin(object):
    def __init__(self, keystone_client):
        self.keystone_client = keystone_client

    def authenticate(self, client, fake_auth_url):
        client.auth_url = fake_auth_url
        client.service_catalog = self.keystone_client.service_catalog
        client.auth_token = self.keystone_client.auth_token
        client.tenant_id = self.keystone_client.tenant_id
        client.management_url = self.keystone_client.service_catalog.url_for(
            attr='region',
            filter_value=client.region_name,
            endpoint_type=client.endpoint_type,
            service_type=client.service_type,
            service_name=client.service_name).rstrip('/')

def getports(user,simulation):
	# Sample output / field mapping
	# </guest/endpoint>-<Sample_Topologies@single-server-WO9N_h>-<csr1000v-1>
	#         USER            PROJECT          TOPOLOGY             NODE
	
	# </advcompnet/endpoint>-<advcompnet-lab1-dcn-scenario1-ymaMSJ>-<veos-4>
	#   USER                  TOPOLOGY                               NODE
	prog=re.compile(r'</(.*)/endpoint>-<(.*)-[_0-9a-z]{6}>-<(.*)>', re.IGNORECASE)

	# table=list()
	try:
		libvirt_uri = os.environ['LIBVIRT_DEFAULT_URI']
	except:
		libvirt_uri = "qemu:///system"
		print "LIBVIRT_DEFAULT_URI env not set!"
		print "Using default '" + libvirt_uri + "'"
	conn=libvirt.openReadOnly(libvirt_uri)
	
	kc = keystone.Client(auth_url=os.environ['OS_AUTH_URL'],
                     username=os.environ['OS_USERNAME'], password=os.environ['OS_PASSWORD'],
                     project_name=os.environ['OS_TENANT_NAME'])
	kc.session.auth = kc
	kc.authenticate()
	nc=nova.Client('2', os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], 
		os.environ['OS_TENANT_NAME'], auth_system='keystonev3', auth_plugin=KeystoneV3NovaAuthPlugin(kc), auth_url='http://fake/v2.0')

	for server in nc.servers.list(search_opts={'all_tenants': True}):
		m=prog.match(server.name)
		if m:
			try:
				domain=conn.lookupByUUIDString(server.id)
			except:
				print "Domain not found / not running"
				return 1
			else:
				doc=parseString(domain.XMLDesc(flags=0))
			# get the VNC port
			#port=doc.getElementsByTagName('graphics')[0].getAttribute('port')
			# get the serial console TCP port
			for i in doc.getElementsByTagName('source'):
				if i.parentNode.nodeName == u'console':
					console=i.getAttribute('service')
			# get the instance name
			name=doc.getElementsByTagName('name')[0].childNodes[0].nodeValue
			# print info
			if simulation == "*":
			        if m.group(1) == user:
			                print m.group(3) + "=" + console
                        else:
			        if m.group(1) == user and server.name.find(simulation) != -1:
			                print m.group(3) + "=" + console
                       

def main():
        if len(sys.argv) != 3:
                sys.stdout.write(str(sys.argv[0]))
                print ": username and simulation (e.g., project name or session-id) needed as argument! bailing out"
                return 1
        else:
                user = str(sys.argv[1]).strip()
                simulation = str(sys.argv[2]).strip()
                getports(user,simulation)
                return 0

if __name__ == '__main__':
	sys.exit(main())

