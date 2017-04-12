=============================
Introduction and Installation
=============================

Purpose
=======

Kunteksto is a tool for helping researchers in the biomedical field translate their CSV formatted data files into the common format of a S3M Data Model so that this data can be used in conjuntion with S3Model clinical and other data in analysis and decision support systems. It also enables expanded semantics for other secondary use of the data based upon the needs of those users.

The importance of this capability is discussed in other S3Model documentation and references. 


Requirements
============

- Python 3.5 or later.
- Installation of SQLiteBrowser. See: http://sqlitebrowser.org/ 
- The requirements.txt file contains all of the Python requirements and can be installed using the *pip* command. 



Installation
============

Install Python 3.5 and SQLiteBrowser. Then ...

Linux
-----

	$ pyvenv --python=python3 ~/Kunteksto
	
	$ cd ~/Kunteksto
	
	$ source bin/activate
	
	$ wget https://github.com/DataInsightsInc/Kunteksto/archive/1.0.0.tar.gz
	
	$ tar -xzf Kunteksto-1.0.0.tar.gz 
	
	$ cd Kunteksto-1.0.0
	
	$ pip install -r requirements.txt 

	$ gedit tradukisto.conf (enter the executable path for SQLiteBrowser, save, exit)
	
	$ python Kunteksto.py


Windows
-------

(coming soon)


Mac OSX
-------

(coming soon)
