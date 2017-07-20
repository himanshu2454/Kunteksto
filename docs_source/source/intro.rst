=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** [#f1]_ is a tool for helping data creators and data users to translate their simple CSV formatted data files into the semantically enhanced formats. This provides a path for existing data to be used in conjuntion with the emerging *data-centric, model first* approach in analysis, general artificial intelligence and decision support systems. This approach opens the door for the change to a *data-centric* world as opposed to the *application-centric* one we have now. This new approach enables automatic interoperability avoiding the data quality issues created through data cleaning and massaging. 

The importance of this capability and improved data quality is discussed in foundational `S3Model <https://datainsights.tech/S3Model>`_ documentation and references. However, detailed understanding of S3Model is not required to understand and use the power of Kunteksto.


Requirements
============

- Python 3.6 or later. See: https://www.python.org/downloads/ 
- Installation of SQLiteBrowser. See: http://sqlitebrowser.org/ 

.. _install:

Installation
============

Linux
-----

Install Python and SQLiteBrowser as directed by the links above. 

Follow the instructions for your platform for lxml installation. See: http://lxml.de/installation.html Because the process can even vary across versions of operating systems, you may need this resource as well: https://stackoverflow.com/search?q=install+lxml 

Now that that is settled.  The rest is easy.  Just create a virtual environment for Python 3.6 or later, using your favorite tool; conda, virtualenv, etc. 

Download and extract the latest release of Kunteksto from GitHub https://github.com/DataInsightsInc/Kunteksto/releases

Activate your virtual environment and navigate to the versioned directory (where you see setup.py) you extracted. For example Kunteksto-1.2.3 and then run:

python setup.py install 

After several minutes of installing all the cool stuff, you'll be ready to begin the tutorial. 


	Go to the :ref:`tutor` 


Windows
-------

Details coming soon. However, if you are a power user you can probably work it out from the Linux instructions.
Just install the pre-requisites and then run *python setup.py install* in a virtual environment.

Mac OSX
-------

Details coming soon. However, if you are a power user you can probably work it out from the Linux instructions.
Just install the pre-requisites and then run *python setup.py install* in a virtual environment.


.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation for *Context*. See: https://simple.wikipedia.org/wiki/Esperanto for more information about the Esperanto language.

