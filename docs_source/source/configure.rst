Configuration
=============

The initial kunteksto.conf file should be okay for most uses and certainly for the demo/tutorials. 

Here we cover the details of the configuration options for those that want to make changes that are more advanced than what is in the simple GUI. 

.. sourcecode:: text

	[SQLITEBROWSER]
	path: /usr/bin/sqlitebrowser

	[KUNTEKSTO]

	; analyzeLevel can be either Simple or Full.
	analyzeLevel: Full

	; set a relative directory for the output selection to open
	outDir: output

	; allowed separator types are one of these:  , ; : | $ 
	sepType: ;

	; allowed values for data format are: XML or JSON
	datafmt: XML

	; NOT YET IMPLEMENTED: A default repository where we can write the output in place of writing to the filesystem.
	; The configuration will check each of these repositories and select the first one that is active. 
	; They will be checked in this order: STARDOG, BLAZEGRAPH, GRAPHDB and ALLEGROGRAPH. 
	; Do not delete the section headers of unused DBs. 
	; To use a DB, set the status: to 'ACTIVE'. Then complete the required information for the ACTIVE DB. 


	[STARDOG]
	status: INACTIVE



	[BLAZEGRAPH]
	status: INACTIVE



	[GRAPHDB]
	status: INACTIVE



	[ALLEGROGRAPH]
	status: INACTIVE


