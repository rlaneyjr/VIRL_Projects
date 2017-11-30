#Testing

###Prerequisite

Install the project
```
$ cd ~/git/cosc-learning-labs/src
$ pip install -e .
```
(Unless a `virtualenv` is active the command above may need to be prefixed with `sudo`.)

##Run the test suite
```
$ cd ~/git/cosc-learning-labs/src
$ python setup.py test –a ../test
```
(Unless a `virtualenv` is active the command above may need to be prefixed with `sudo`.)

The first time the test suite is run, the setup.py file is needed because it knows which Python libraries  
the test code depends upon (including the pytest module). These dependencies will be installed if necessary 
(hence the need for `sudo`).

In the command above, `python` can be replaced with any variation such as `python3` or `../env/bin/python`. 
The `-a ../test` instructs the `pytest` module to look for test cases in the sibling directory named `test`.

The test suite can subsequently be run using the command
```
$ cd ~/git/cosc-learning-labs/test
$ python -m pytest
```
or, if not in the test directory then specify the test directory location explicity
```
$ cd ~/git/cosc-learning-labs/test
$ python -m pytest ../test
```

Sample output
```
$ cd ~/git/cosc-learning-labs/test
$ python -m pytest
============================= test session starts ==============================
platform linux2 -- Python 2.7.6 -- py-1.4.27 -- pytest-2.7.0
rootdir: /home/virl/git/cosc-learning-labs/test, inifile: 
collected 4 items 

test_device_dismount.py .
test_device_mount.py .
test_interface_configuration.py .
test_interface_names.py .

=========================== 4 passed in 3.93 seconds ===========================
```

###Using `pytest` directly

In the section above, the command that is executed directly is `python` and `pytest` is run indirectly via 
the Python interpreter.

`pytest` may be run directly but doing so is not supported by this project. 


To install `pytest` as a command (not a Python module)
```
pip install pytest
```
(possibly with a `sudo` prefix)
```
$ cd ~/git/cosc-learning-labs/test
$ pytest
```
or, if not in the test directory, specify the test directory location explicity
```
$ cd ~/git/cosc-learning-labs/src
$ pytest –t ../test
```
Sample output
```
$ cd ~/git/cosc-learning-labs/test
$ pytest
=====================  test_interface_names.py  ======================
sleep(0.2) seconds pending connection to 1 network device(s).
sleep(0.4) seconds pending connection to 1 network device(s).
1 network device connection(s) verified after 3 check(s) and 0.6 seconds.
.
=================  test_interface_configuration.py  ==================
.
=======================  test_device_mount.py  =======================
.
=====================  test_device_dismount.py  ======================
.
*******************************************************************************
Ran 4 test cases in 4.57s (0.13s CPU)
All 4 modules OK
```
