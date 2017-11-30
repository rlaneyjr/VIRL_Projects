#!/usr/bin/env python

import requests
import sys

odl_user = 'admin'
odl_pass = 'admin'

request_template = '''<?xml version="1.0" encoding="UTF-8"?>
<module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
	<type
		xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
	<name>%s</name>
	<address
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</address>
	<port
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</port>
	<username
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</username>
	<password
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</password>
	<tcp-only
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">false</tcp-only>
	<event-executor
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
		<type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
		<name>global-event-executor</name>
	</event-executor>
	<binding-registry
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
		<type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
		<name>binding-osgi-broker</name>
	</binding-registry>
	<dom-registry
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
		<type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
		<name>dom-broker</name>
	</dom-registry>
	<client-dispatcher
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
		<type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
		<name>global-netconf-dispatcher</name>
	</client-dispatcher>
	<processing-executor
		xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
		<type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">
			prefix:threadpool</type>
		<name>global-netconf-processing-executor</name>
	</processing-executor>
</module>
'''

request_body = request_template % (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

headers = { 
'Content-Type' : 'application/xml',
'Content-Length' : "%d" % (len(request_body)),
'Accept' : 'application/json' }

url = 'http://' + sys.argv[1] + ':8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules'

resp = requests.post(url, data=request_body, headers=headers, auth=(odl_user, odl_pass))
print resp
