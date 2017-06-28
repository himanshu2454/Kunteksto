Configuration
=============

The initial kunteksto.conf file should be okay for most uses and certainly for the demo/tutorials. 

Here we cover the details of the configuration options for those that want to make changes. 

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

; NOT YET IMPLEMENTED: A default repository where we can write the output in addition to the filesystem.

[TINKERGRAPH]
repository: None

[STARDOG]
repository: None

[BLAZEGRAPH]
repository: None
