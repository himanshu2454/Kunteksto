=============
Configuration
=============

The initial kunteksto.conf file should be okay for most uses and certainly for the demo/tutorials. 

.. _config:

Config File Details
===================
Here we cover the details of the configuration options. 

.. sourcecode:: text

	; kunteksto.conf is the configuration file required by Kunteksto. 

	[SQLITEBROWSER]
	; Enter the command or full path required to execute SQLite Browser on your system.
	cmd: sqlitebrowser


For Windows users you need to put it in quotes because of the spaces

.. sourcecode:: text

	cmd: "DB Browser for SQLite.exe"

Depending upon your OS and installation you may need the full path to the SQLite Browser executable and you may need to adjust access permissions.

.. sourcecode:: text

	[KUNTEKSTO]
	
	; analyzelevel can be either Simple or Full.
	analyzelevel: Full

	; allowed delimiter (field separator) types are one of these:  , ; : | $ 
	; The default delimiter is defined here.
	delim: ;

	; A default output directory may be defined here. It can be overridden on the commandline.
	; The 'output' directory is relative to the installation directory of Kunteksto. 
	; Typically it is only used for the Demo and Tutorials.
	outdir: output

These three items are also available on the commandline. A commandline entry will override these defaults.


.. sourcecode:: text


	; Default data formats to create. Values are True or False.
	xml: True
	rdf: True
	json: True

These values determine what data file format(s) will be generated.  If a file format is set to *True* and no repository is configured for that format; then the files will be written to the filesystem under the defined *outdir*.  


.. sourcecode:: text


	[NAMESPACES]
	; any additional namespaces must be defined here with their abbreviations. 
	; {abbrev}:{namespace URI}

	dul: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl# 

When defining the semantics for your models you will want to use appropriate ontologies from various sources such as Linked Open Vocabularies http://lov.okfn.org/dataset/lov  Biontology https://www.bioontology.org/ etc. As well as your own local ontologies. You must define an abbreviation for each ontology namespace here. The one above shows the example from the Tutorial/Demo of defining the *dul* abbreviation for the Ontology Design Patterns ontology.  

.. sourcecode:: text


	; Below are where repository setups are defined for each of the three types of data generation.
	; If a type is to be generated but no repository is defined for the type. Then the data will be generated 
	; and written to the filesystem in a subdirectory of the output directory.  


	; A default repository where we can write the output XML instead of to the filesystem.
	; The config will only process the first one with an ACTIVE status. 

	[BASEX]
	status: INACTIVE
	host: localhost
	port: 1984
	dbname: S3M_test
	user: admin
	pw: admin

	; Not Yet Implemented
	[EXISTDB]
	status: INACTIVE


	; A default repository where we can write the output RDF instead of to the filesystem.
	; The config will only process the first one with an ACTIVE status. 
	 

	[ALLEGROGRAPH]
	status: INACTIVE
	host: localhost
	port: 10035
	repo: S3M_test
	user: admin
	pw: admin

	; Not Yet Implemented
	[STARDOG]
	status: INACTIVE

	; Not Yet Implemented
	[BLAZEGRAPH]
	status: INACTIVE

	; Not Yet Implemented
	[GRAPHDB]
	status: INACTIVE


	; A default repository where we can write the output JSON instead of to the filesystem.
	; The config will only process the first one with an ACTIVE status. 

	[MONGODB]
	status: INACTIVE
	host: localhost
	port: 27017
	dbname: S3M_test
	; default MongoDB has no authentication requirements.
	user: admin
	pw: admin

	; Not Yet Implemented
	[COUCHDB]
	status: INACTIVE

There is currently one repository supported for each filetype. We plan to support the others in the future. 


**There are no user editable options in the SYSTEM section.**

.. sourcecode:: text


	[SYSTEM]
	version: 1.2.5
