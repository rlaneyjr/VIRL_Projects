# Extract network topology from interface descriptions

The *extract-links* Ansible playbook uses interface descriptions to generate list of links within the network. It assumes that all links (node-to-node and node-to-LAN) have description "to *remotenode*" (as generated by VIRL). If you use a different naming convention, play with the `set remote=...` statement in Jinja2 templates.

The playbook uses snmp_facts to get interface descriptions.

## Multi-vendor support (on your own)

The *extract-links* playbook works on any devices that support SNMP MIB II. The *config-enable-snmp.yml* playbook works with Cisco IOS, but feel free to extend it to any other operating system.

## Usage

* Create your inventory file (**hosts** in the current directory)
* Change usernames and SNMP community in group_vars/all.yml. Even better, use SSH keys instead of hard-coded usernames and passwords.

* Configure SNMP community on Cisco IOS devices if needed:
```
ansible-playbook config-enable.snmp.yml
```
* Check that SNMP works as expected
```
ansible-playbook extract-links.yml -t facts
```
* Generate the links file with
```
ansible-playbook extract-links.yml
```
* Enjoy, modify and submit a pull request when you add something awesome