=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** [#f1]_ is a tool for helping data creators and data users to translate their simple CSV formatted data files into the semantically enhanced format of a S3M Data Model. This provides a path for data to be used in conjuntion with other S3Model data in analysis and decision support systems. It also enables expanded semantics so that secondary users can better determine if the data is appropriate for their needs. The S3Model approach opens the door for the change to a data-centric world as opposed to the current application-centric one we have now. This new world will allow automatic interoperability without the need for data cleaning and massaging. 

The importance of this capability and improved data quality is discussed in other `S3Model <https://datainsights.tech/S3Model>`_ documentation and references. 


Requirements
============

- Python 3.5 or later.
- Installation of SQLiteBrowser. See: http://sqlitebrowser.org/ 
- The requirements.txt file contains the Python requirements and can be installed (see below) using the *pip* command.
- A copy of the S3Model Reference Model schema s3model_3_0_0.xsd 


.. _install:

Installation
============

Install Python 3.5 or later and SQLiteBrowser. Then setup a virtual environment. 

If you are using Anaconda you can create a new environment using:

*conda create --name Kunteksto python=3* 

Activate it using *source activate Kunteksto* then skip to number 4. 

Otherwise use pyenv as shown below.   

See `this StackOverflow post <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_ about the various environment options for Python 3.x 

Linux
-----

	#. $ pyvenv --python=python3 ~/Kunteksto
	
	#. $ cd ~/Kunteksto
	
	#. $ source bin/activate
	
	#. $ wget https://github.com/DataInsightsInc/Kunteksto/archive/1.2.0.tar.gz
	
	#. $ tar -xzf Kunteksto-1.2.0.tar.gz 
	
	#. $ cd Kunteksto-1.2.0
	
	#. $ pip install -r requirements.txt 

	#. Using your favorite text editor, open tradukisto.conf (Edit the path for the SQLiteBrowser executable if it is different on your system. For now you can leave the other options as defaults. Save & exit.)
	
	#. $ python kunteksto.py

	Go to the :ref:`tutor` 


Windows
-------

(coming soon)


Mac OSX
-------

(coming soon)


.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation for *Context*. See: https://simple.wikipedia.org/wiki/Esperanto for more information about the Esperanto language.

