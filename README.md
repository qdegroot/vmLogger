# vmLogger
Designed to be "set and forget". Attempts to connect to a series of vmHosts provided through CSV in a vSphere environment and create a self-limiting set of logs over an indefinite number of scheduled runs.

Note: This was created to be run within a specific hospital system's network and setup.
Probably ineffective for general use. ReadMe was initially written to be internal.


Environment Logger Summary
==========================

Dependencies:   Python 3.X
		pyVmomi
		connect_info.csv
		
		
pyVmomi:
	>'pip install pyvmomi'
Materials=>connect_info.csv:
	>one hostname per row. Domain necessary.
Materials=>write_list:
	>log of the past few files written. However many filenames are written here when the whole system is set is how many logs        the program will keep. 

===========
USAGE
===========

Run daily, read logs in Logs folder the program generates if you feel like it.

-To change hosts logged: add lines to connect_info.csv, delete hostnames if you feel like it, please no blank lines
-To change username and password: open env_logger.py with your favorite editor and change the user and pwd vars at the end
-To change number of log files the program keeps: add fake filenames to the top of write_list
