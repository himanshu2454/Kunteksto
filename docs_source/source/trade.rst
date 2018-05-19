
The original data set is provided by `UNdata <http://data.un.org/Explorer.aspx>`_

The best source of this data is the `Kaggle Competition <https://www.kaggle.com/unitednations/global-commodity-trade-statistics>`_


The details of the original data source and other information are located on the site. This information may be useful in filling in the database *model* and *record* tables. The *Column Metadata* tab on the download page has some of the information for each record. 

`Download the dataset <https://www.kaggle.com/unitednations/global-commodity-trade-statistics/data>`_ Extract the CSV data and place it the *kunteksto/example_data* directory.


Following the same step by step procedures outlined in the *Getting Started* section.


- Navigate to the directory where you installed Kunteksto.

- Be certain the virtual environment is active.

.. caution::

    If you closed and reopened a new window, then you need to activate the environment again. Also, be sure that you are in the *kunteksto* directory. 


    **Windows**

    .. code-block:: sh

        activate <path/to/directory> 

    **or Linux/MacOSX**

    .. code-block:: sh

        source activate <path/to/directory> 


For this tutorial, you start Kunteksto in prompt mode. 

.. code-block:: sh

    kunteksto


These mandatory items will be requested:

	- At the **Enter a valid mode:** prompt, type *all*

	- At the **Enter a valid CSV file:** prompt, type *example_data/commodity_trade_statistics_data.csv* 


Kunteksto analyzes the input file and creates a results database in the *output* directory.

The output RDF will be in the Kunteksto repository in AllegroGraph which you can explore through the AllegroGraph WebView browser tool or using `Gruff <https://franz.com/agraph/gruff/>`_ which I **HIGHLY** recommend. You can also explore the XML using the `BaseX GUI <http://basex.org/basex/gui/>`_. 

There are many written and video tutorials on using these tools. Check the `AllegroGraph YouTube Channel <https://www.youtube.com/user/AllegroGraph/videos>`_ and the `BaseX Getting Started <http://docs.basex.org/wiki/Getting_Started>`_.


