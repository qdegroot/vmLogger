# vmLogger
Designed to be "set and forget". Attempts to connect to a series of vmHosts provided through CSV in a vSphere environment and create a self-limiting set of logs over an indefinite number of scheduled runs.

Note: This was created to be run within a specific hospital system's network and setup.
Probably ineffective for general use. ReadMe was initially written to be internal.


Environment Logger Summary
==========================

Dependencies:   Python 3.X
		pyVmomi
		connect_info.csv
		
		

Python 3.x:
	>Available for free download from the web
	>Make sure to add python to PATH variable for command line
pyVmomi:
	>Once python 3.x is available, use the command 'pip install pyvmomi' to install pyvmomi
Materials=>connect_info.csv:
	>one hostname per row
Materials=>write_list:
	>log of the past few files written. Automatically updates, pls no touch.
Logs:
	>Past few logs saved here by date.

===========
USAGE
===========

Run daily, read logs in Logs folder if you feel like it.

-To change hosts logged: add lines to connect_info.csv, delete hostnames if you feel like it, please no blank lines
-To change username and password: open env_logger.py with your favorite editor and change the user and pwd vars at the end
