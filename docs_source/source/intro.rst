=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** (ˈkänˌteksto) [#f1]_ is a tool for helping domain experts, data creators and data users translate their simple CSV formatted data files into the semantically enhanced formats. This provides a path for existing data to be used in conjuntion with the emerging *data-centric, model first* approach in analysis, general artificial intelligence and decision support systems. This approach opens the door for the change to a *data-centric* world as opposed to the *application-centric* one we have now. This new approach enables automatic interoperability avoiding the data quality issues created through data cleaning and massaging. 

The importance of this capability and improved data quality is discussed in foundational `S3Model <https://datainsights.tech/S3Model>`_ documentation and references. However, detailed understanding of S3Model is not required to understand and use the power of Kunteksto. Addtional information on the data-centric movement can be found below [#f2]_

Target Audience
---------------
Kunteksto design is based around the ability for *domain experts* from any field, with very little programming ability to quickly annotate data extracts to improve the usability of the data.  Data engineers and data scientists can also benefit from Kunteksto in the same ways as domain experts. It just takes a bit more research to discover the semantics.

Requirements
============

- Python 3.6 or later. See: https://www.python.org/downloads/ 
- Installation of SQLiteBrowser. See: http://sqlitebrowser.org/ or other tool for editing SQLite databases.

.. _install:

Installation
============

Cross-Platform on Anaconda
--------------------------

This is the **preferred environment** for a tool like Kunteksto because it integrates easily with systems for domain experts, data engineers and data scientists.

- Install Anaconda Python 3.5+ for your platform according to the instructions here https://docs.continuum.io/anaconda/install/ 
- Install SQLiteBrowser as directed by the links above. 
- If you are using Linux or Mac OSX, follow the instructions for your platform for lxml installation. See: http://lxml.de/installation.html

- Create a conda environment: 

.. code-block:: sh

    conda create -p kunteksto python=3

- Change to the directory e.g. *cd kunteksto*
- Activate the environment 
- pip install kunteksto

These four quick steps creates a virtual environment in the subdirectory *kunteksto*. When it is created conda displays how to activate the environment. Once activated then Kunteksto is installed in the subdirectoy along with the environment. 

The last step is to do the :ref:`tutor`



Windows
-------

Details coming soon. Preferably use the Anaconda instructions. 


Mac OSX
-------
Follow the instructions for your platform for lxml installation. See: http://lxml.de/installation.html 

Details coming soon. Preferably use the Anaconda instructions. 


Linux
-----

Install Python and SQLiteBrowser as directed by the links above. 

Follow the instructions for your platform for lxml installation. See: http://lxml.de/installation.html 

Now that that is settled.  The rest is easy.  Just create a virtual environment for Python 3.6 or later, using your favorite tool; conda, virtualenv, etc. 

.. code-block:: sh

    conda create -p kunteksto python=3

Activate your virtual environment and navigate to the *kunteksto* directory. Then install kunteksto using pip.

.. code-block:: sh
 
    pip install kunteksto

After several minutes of installing all the cool stuff, you'll be ready to begin the tutorial. 


	Go to the :ref:`tutor` 


.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation for *Context*. See: https://simple.wikipedia.org/wiki/Esperanto for more information about the Esperanto language.

.. [#f2] 
    -  The Estes Park Group http://estesparkgroup.org/
    -  The Data-centric Manifesto http://datacentricmanifesto.org/
    -  Data-centric companies will devour competitors https://goo.gl/xDcpZM
    -  The Data-Centric Revolution: Gaining Traction https://goo.gl/zdRLm9
    -  The limits of deep learning https://blog.keras.io/the-limitations-of-deep-learning.html 
    -  The future of deep learning https://blog.keras.io/the-future-of-deep-learning.html