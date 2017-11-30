# How This Code is Organised

The Python code consists of two main modules: `basics` and `learning\_lab`. The `basics` code wraps the HTTP requests for the controller RESTCONF interfaces, handling errors and data formatting, and providing a set of functions that can be called from the `learning\_lab` code. The `learning\_lab` code shows how to use the basic functions and groups them thematically.

The `settings` module contains configuration files, which are also Python code, to define where a given controller instance is, and which Netconf devices it should mount. You should edit/create a suitable configuration file for your environment, and then set the `NETWORK_PROFILE` environment variable to the name of that file, e.g.:

```bash
$ export NETWORK_PROFILE=dcloud_v2
``` 

# Using the Learning Lab Code

You should `cd` into the learning\_lab directory, where you will be able to run scripts in the lab, as below:

* 01_inventory_mount.py – Causes the server to use Netconf to mount the XRv instances in the ../settings/dcloud.py configuration file.

```bash
$ ./01_inventory_mount.py 
Python Library Documentation: function device_mount in module basics.inventory
device_mount(device_name, device_address, device_port, device_username, device_password)
Add the specified network device to the inventory of the Controller.
device_mount(lax, cisco, cisco, 830, 198.18.1.51)\n
device_mount(san, cisco, cisco, 830, 198.18.1.54)\n
device_mount(sea, cisco, cisco, 830, 198.18.1.55)\n
device_mount(min, cisco, cisco, 830, 198.18.1.52)\n
device_mount(por, cisco, cisco, 830, 198.18.1.53)\n
device_mount(sjc, cisco, cisco, 830, 198.18.1.57)\n
device_mount(kcy, cisco, cisco, 830, 198.18.1.50)\n
device_mount(sfc, cisco, cisco, 830, 198.18.1.56)\n
```

*	01_inventory_connected.py – Displays the connected devices:

```bash
$ ./01_inventory_connected.py 
Python Library Documentation: function inventory_connected in module basics.inventory
inventory_connected()
    Names of network devices connected to the Controller.
    Output a list of names.
    Connected devices are a subset of the inventory.
['sea', 'por', 'san', 'lax', 'sjc', 'sfc', 'kcy', 'min']
```

The output above indicates that the controller has mounted the XRv devices, and that all devices connected properly. If you do not see that they connected properly, try again. It can take a several minutes for all of the network elements to mount and connect.
After that, there are additional sets of scripts to examine certain components and set properties on those components, as appropriate. 

To see which scripts there are, use the “ls” command as shown below (note that this is a just an elided example of what you will see, as the contents will change over time): 

```bash
$ ls
00_controller.py 01_inventory_unreachable.py 04_static_route_json_all.py
00_devices.py	 02_capability.py 04_static_route_list.py
00_settings.py 02_capability_compare.py	04_static_route_suite.py
01_device_connect.py 02_capability_discovery.py 04_topology.py
01_device_connected.py 02_capability_matrix.py	05_acl_apply_packet_filter.py
01_device_control.py 03_interface_configuration.py 05_acl_capability.py
…
```

Some of what these scripts cover includes:  

* Inventory
* Netconf/Yang capabilities
* Interfaces
* Routes and Topology
* ACLs

This is a living body of code, and so can vary each time you use this lab.

If you want to modify the list of devices being mounted, edit the ../settings/dcloud.py file. That file is Python code as well.
You can also use the inbuilt Python interpreter to call the functions in the basics library, in the same way that the code in the learning_lab directory does, and you can adapt and modify any of the scripts that you as you like. You will not break anything.

Have at it! 

The Cisco DevNet team – developer.cisco.com.

# Troubleshooting

Some problems that can arise when working with the Open SDN Controller are discussed below:

* Chrome caches the progress bar and does not move beyond that when accessing the GUI of the controller. If you have Firefox available, then use that.
* The controller becomes un-responsive, or responds with 50X errors. This can happen for a variety of reasons, and the simple remedy is to reboot the controller VM as shown below.
*	The network is in some state, with routes, ACLs, interfaces shutdown, or similar, probably because of a previous series of exercises with the same lab instance, that leads to unexpected results. In this case there is a `restore_network_state.py` script that should reset everything and leave the controller with no mounted devices. If this script does not work, reboot the controller server and try again after five minutes.
	


I want to clarify that the sample scripts are deliberately as simple as possible.

Where there is a requirement for additional functionality then it will be provided in a separate script. That is one reason we have a lot of scripts (50+).

I bend the rules a little bit when a function can return None. In those situations I continue to call the function until the output is interesting.

For example, we might continue sampling network interfaces until we find one that has an ip address.

People will be running the sample scripts and then examining all the HTTP requests and responses. For the elemental sample scripts there will ideally be no more than 3 HTTP requests.

As we build comprehensive/composite scripts there will be too many HTTP requests and we will not make them available. It is too much information. Instead we will refer people to the elemental scripts.

So, if you see sample code like:

for device in inventory:
	if demonstrate(device):
		stop

Then you know why that loops stops asap.


The instructions are in file:

	doc/guide/sandbox.pdf

Notes about ordering of scripts.

Suggested order of ‘groups’ of scripts is by numeric prefix:

01 inventory
02 capabilities
03 interface
04 ACL

Within each group the suggested order of scripts can be seen in this file (which we visited in the webex):

http://gerrit-open1.cisco.com/gerrit/gitweb?p=cosc-learning-labs.git;a=blob;f=src/learning_lab/suite.py;hb=HEAD

Right now the ‘suite’ does not have ACL so I will make that a top priority.

Hints: to get the network into a particular state the following two scripts are useful:

01_inventory_mount.py

01_inventory_dismount.py

You will see that I use these two scripts a lot in ‘suite’ to establish a specific context.

Note: each script tries to demonstrate one simple thing. We don’t want a one line script performing ten lines of ‘setup’ or ’tear down'. Therefore, each script tries to do its thing but may not succeed.

E.g.mount one device. If all devices are already mounted then it does nothing except print a message on stdout.

I have been evolving an idea that each script returns normally (exit code 0) when it succeeds and abnormal (exit code 1) when it is unable to demonstrate/proceed. Some scripts have this but not all (yet).

Example of usage: run script 01_device_dismount until the exit code is non-zero. All devices are thus not mounted.

Notes on terminology: 

Mount: verb, introduce a device to the controller and attempt connection.
Dismount: verb, complement of mount
Mounted: adjective, the ‘mount’ operation was applied
Unmounted: adjective, available to ‘mount’, unknown to controller, specified in settings/config

PS: we did not discuss the HTTP layer but it is considered by some people to be of importance. One of the constructive criticisms of the LL many months ago was that it did not teach people how to communicate with ODL/COSC using HTTP. We responded by capturing the HTTP requests and responses that occur as the Python (high level) library API is used. The HTTP details appear in the HTML pages.

Here is a sample link to a HTML page where the HTTP details can be seen:

http://nbviewer.ipython.org/url/gerrit-open1.cisco.com/gerrit/gitweb/%3Fp%3Dcosc-learning-labs.git%3Ba%3Dblob_plain%3Bf%3Dsrc/notebook/01_device_connected.ipynb%3Bhb%3DHEAD

Notes on settings: the scripts prefixed with 00 are for administrative purposes. They don’t modify anything (so far) – they just report. They inform you about the settings that the Python sample scripts will ‘see’.

Notes on known bugs:

Modifying interface configuration does not currently succeed if there is no IP address. I will try to fix this by omitting the XML element for the IP address when there is no IP address.

Notes on Python 2 and 3:

All the sample scripts in groups 01, 02 and 03 run in both Python 2 and 3. Group 04 is currently Python 2 only.

Notes on capability and device versions:

Network devices have different capabilities for each version. The sample scripts are currently not sophisticated at checking if a required capability is supported by an individual device. The sample scripts will fail if there is a capability/version mismatch. We have some excellent work in the pipeline to address this issue in an elegant and robust manner. For example, query the inventory for all devices with a specific capability.

I have put this text into the README.txt file, which is here:

http://gerrit-open1.cisco.com/gerrit/gitweb?p=cosc-learning-labs.git;a=blob;f=README.txt;hb=HEAD

