from __future__ import print_function as _print_function
from basics.acl import acl_create_port_grant, acl_list, acl_json, acl_delete, _url_template
from basics.acl_apply import acl_apply_packet_filter
from basics.odl_http import odl_http_get, odl_http_post
import json
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

_acl_route_request_content = '''{"Cisco-IOS-XR-ipv4-acl-cfg:accesses" : [{"access":[
{"access-list-name": "%s", 
  "access-list-entries": {
    "access-list-entry": [
      {
        "source-network": {
          "source-wild-card-bits": "%s", 
          "source-address": "%s"
        }, 
        "next-hop": {
          "next-hop-1": {
            "next-hop": "%s"
          }, 
          "next-hop-type": "regular-next-hop"
        }, 
        "sequence-number": 10, 
        "grant": "permit"
      }, 
      {
        "sequence-number": 20, 
        "grant": "permit"
      }
    ]
  }
}
]}]}
'''

def demonstrate(device_name):
    url_suffix = _url_template % quote_plus(device_name)
    url_params = {}
    contentType = 'application/json'
    accept = contentType
    expected_status_code = [204, 409]
    source_address = '1.0.0.0'
    source_wild_card_bits = '0.255.255.255'
    next_hop = '4.3.2.1'
    access_list_name = quote_plus('policy-route-http')
    content = _acl_route_request_content % (access_list_name, source_wild_card_bits, source_address, next_hop)
    print('acl_next_hop(%s)'%device_name)
    response = odl_http_post(url_suffix, url_params, contentType, content, accept, expected_status_code)
    if response.status_code != 204:
        print(response)
    else:
        print('ACLs:', acl_list(device_name))
        print(json.dumps(acl_json(device_name, access_list_name), indent=2))

from basics.acl import inventory_acl
for device_name in inventory_acl():
    demonstrate(device_name)
