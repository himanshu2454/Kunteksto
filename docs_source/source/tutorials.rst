
.. _advtutor:

==================
Advanced Tutorials
==================

Below are additional tutorials to perform after the **Getting Started** :ref:`tutor`.


These tutorials require the installation of the `AllegroGraph <https://franz.com/agraph/downloads/?ui=new>`_ database and the `BaseX <http://basex.org>`_ database. 

If you are not familiar with semantic graph datases please see the `AllegroGraph Documentation <https://allegrograph.com/support/documentation/current/agraph-introduction.html>`_ 

 Optionally, you may install `MongoDB <https://www.mongodb.com/>`_ to persist the generated JSON files.


Prerequisites
=============

BaseX
-----
BaseX requires Java 8 for your platform.

Please `download the ZIP file <http://basex.org/download/>`_ and extract it into your home directory. 

Start the server using the `Client/Server instructions <http://docs.basex.org/wiki/Startup>`_. You will use the client in later parts of the tutorial.  


AllegroGraph
------------

`Download and Install the server for your platform based on these instructions <https://franz.com/agraph/downloads/?ui=new>`_ . 

When asked for the superuser username and password use these:

.. code-block:: sh

    user: admin
    password: admin

If you use another username or password, you must edit the entries in kunteksto.conf using a text editor. See below for editing kunteksto.conf. 

When the server is installed and running, install the `Gruff GUI client <https://franz.com/agraph/gruff/download/index.clp?ui=new>`_ for AllegroGraph. You will use this later in the tutorials.


.. caution::

    Only edit the configuration file with a text editor. Do not use a word processing application such as MS Word or LibreOffice. There are many great text editors from which to choose.  Some favorites, in no particular order, are:

        - `Atom <https://atom.io/>`_
        - `VS Code <https://code.visualstudio.com/>`_
        - `Sublime <https://www.sublimetext.com/>`_



Configuration
-------------

Using a text editor, edit the *status* entries in kunteksto.conf for [BASEX] and [ALLEGROGRAPH]. Change them from INACTIVE to ACTIVE. When completed they should look like this:

For BaseX:

.. sourcecode:: text

    [BASEX]
    status: ACTIVE
    host: localhost
    port: 1984
    dbname: Kunteksto
    user: admin
    password: admin


For AllegroGraph:

.. sourcecode:: text

    [ALLEGROGRAPH]
    status: ACTIVE
    host: localhost
    port: 10035
    repo: Kunteksto
    user: admin
    password: admin


Unless you are using MongoDB for JSON persistence you will likely want to turn off JSON generation.

.. sourcecode:: text

	; Default data formats to create. Values are True or False.
	; These can be changed in the UI before generating data. 
	xml: True
	rdf: True
	json: False


Database Checks
---------------
From the kunteksto directory run

.. code-block:: sh

    python utils/db_setup.py

This python script tests the database connections and installs the S3Model ontology and 3.1.0 Reference Model RDF.

During execution, the script displays several lines of output to the terminal. Specifically look for *AllegroGraph connections are okay.* and *BaseX connections are okay.* or any lines that start with **ERROR:**.

.. caution::

    If you see the *okay* output lines and no **ERROR:** lines, then all went well. Otherwise, you must troubleshoot these issues before continuing. 


Viewing the RDF Repository
--------------------------

You can view the Kunteksto repository by using `this link <http://127.0.0.1:10035/#/repositories/Kunteksto>`_ in a browser. 
Right click and open it in a new tab. Then under **Explore the Repository** click the *View Triples* link. 
These triples are the S3Model ontology and the S3Model 3.1.0 RDF. These triples connect all of your RDF into a graph, 
even when they do not have other semantics linking them. 

You may also use the Gruff GUI Client to explore the respoitory at any time. See the `Franz, Inc. Learning Center <https://franz.com/agraph/gruff/learning-center.lhtml>`_ for more information.



.. _honeytutor:

US Honey Production
===================


.. include:: honey.rst



.. _tradetutor:

Global Commodity Trade Statistics
=================================


.. include:: trade.rst
