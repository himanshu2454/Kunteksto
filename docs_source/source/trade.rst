
The original data set is provided by `UNdata <http://data.un.org/Explorer.aspx>`_

The best source of this data is the `Kaggle Competition <https://www.kaggle.com/unitednations/global-commodity-trade-statistics>`_


The details of the original data source and other information are located on the site. This information may be useful in filling in the database *model* and *record* tables. The *Column Metadata* tab on the download page has some of the information for each record. 

`Download the dataset <https://www.kaggle.com/unitednations/global-commodity-trade-statistics/data>`_ Extract the CSV data and place it anywhere you like. 


Following the same step by step procedures outlined in the *Getting Started* section.


- Navigate to the directory where you installed Kunteksto.

- With the virtual environment active.

.. caution::

    If you closed and reopened a new window, then you need to activate the environment again. Also, be sure that you are in the kunteksto directory. 

    **Windows**

    .. code-block:: sh

        activate <path/to/directory> 

    **or Linux/MacOSX**

    .. code-block:: sh

        source activate <path/to/directory> 


For this tutorial, you start Kunteksto in prompt mode. These mandatory items will be requested:

.. code-block:: sh

    kunteksto


- At the **Enter a valid mode:** prompt, type *all*

- At the **Enter a valid CSV file:** prompt, type *<location of the file>/commodity_trade_statistics_data.csv* 

- Kunteksto analyzes the input file and creates a results database in the *output* directory.

Now explore the RDF data in your graphDB or the XML or JSON data in a DB of your choice.

If you haven't yet chosen repositories for this data here are some suggestions, in no particular order.


**RDF**

`MarkLogic <https://docs.marklogic.com/guide/semantics/intro>`_

`AllegroGraph <https://franz.com/agraph/allegrograph/>`_

`StarDog <https://www.stardog.com/>`_


**XML**

`BaseX <http://basex.org/>`_

`eXistDB <http://exist-db.org/exist/apps/homepage/index.html>`_

**JSON**

`MongoDB <https://www.mongodb.com/>`_

`CouchDB <http://couchdb.apache.org/>`_

There are many other options for persistence depending on your needs. For example, you could use `PostgreSQL <https://www.postgresql.org/>`_ to persist your XML or JSON data.


