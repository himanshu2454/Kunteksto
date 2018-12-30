=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** (ˈkänˌteksto) [#f1]_ is a tool to translate simple CSV formatted data files into computable, semantically enhanced knowledge representations. As a foundation for **crowdsourced**, *automated knowledge base construction*; it provides a path for existing data sets to be used in conjunction with the emerging *graph data, model first* approach in analysis, general artificial intelligence (AGI), and decision support systems. This approach opens the door for the change to a more data-centric approach as opposed to the current application-centric approach. This new path enables automatic, machine processable interoperability avoiding the data quality issues created through data migration, data cleaning and data massaging. See :ref:`mlai`

The importance of how this simplifies query and analysis capabilities and improves data quality is discussed in foundational 
`S3Model <https://datainsights.tech/S3Model>`_ documentation and references. However, detailed understanding of S3Model is not 
required to understand and use the power of Kunteksto. 

Target Audience
---------------
The Kunteksto design philosophy is based on the ability for *domain experts* from any field, with very little programming ability to quickly annotate data extracts to improve the usability of the data. Data engineers and data scientists can also benefit from Kunteksto in the same ways as domain experts. 

Kunteksto can be used in a pipeline to take any existing CSV data sources and create valid XML, JSON and or RDF triples that do not lose the context of the source batch/document and adds specific semantics as selected (one time) by the domain expert. 

.. image:: _images/pipeline.png
    :width: 600px
    :align: center
    :height: 400px
    :alt: JSON Invalid

The above diagram shows how data extracts can be converted to rich semantic data. You may or may not need an OpenRefine macro to clean the data. Once a model is defined in Kunteksto, these consistent CSV files are pipelined through to create one or more of the serializations of the data including all of the semantics defined by the domain expert.


.. _install:

Installation
============

Cross-Platform on Anaconda
--------------------------

Anaconda is the **preferred environment** for a tool like Kunteksto because it integrates easily with systems for domain experts, data engineers, and data scientists.

- `Download and install <https://www.continuum.io/downloads>`_ Anaconda Python 3.7+ for your platform.
- More detailed Anaconda instructions are `here <https://docs.continuum.io/anaconda/install/>`_  if you prefer.

.. note::
    Anaconda now offers to install the `VS Code editor <https://code.visualstudio.com/download>`_. Unless you already have a preferred text editor,
    this is a good choice.

- Download the latest release from `GitHub <https://github.com/DataInsightsInc/Kunteksto/releases>`_.

- Open a terminal window and create a conda environment. On Windows it is best to open an *Anaconda Prompt* terminal from the Anaconda menu: 

.. code-block:: sh

    conda create -n Kunteksto pycurl ujson

- Unpack the downloaded release archive and change to the directory

.. code-block:: sh
    
    cd Kunteksto-x.x.x

Where x.x.x is the Kunteksto release number.


.. _activate: Activate


- Activate the environment according to the **instructions shown by Anaconda in the terminal window**.

Depending upon the options you selected when installing Anaconda:

**Cross Platform**

.. code-block:: sh

    conda activate Kunteksto

**Windows**

.. code-block:: sh

    activate Kunteksto 

**or Linux/MacOSX**

.. code-block:: sh

    source activate Kunteksto 


- Install Kunteksto with this command:

.. code-block:: sh

    python setup.py install

.. warning::

    Occassionaly there will be a network timeout when searching for packages to install. The error will show up as a package not being found. Just re-run the installation command to retry. You will know when it is complete when you see the message *Finished processing dependencies for kunteksto==x.x.x*


Change to the *Kunteksto working directory*:

.. code-block:: sh
    
    cd kunteksto

This is the directory used for all Kunteksto commands. 


The next step is to do the :ref:`tutor`


What are all the files for?
===========================

Depending on how and where you installed Kunteksto you will see a varying number of files and subdirectories. Many of them may be part of the Anaconda environment, so we do not cover those.

Referenced from the *kunteksto* directory created at install time:

Files
-----

- README.md
    A brief explanation of Kunteksto's purpose and links to background information.

- LICENSE.txt
    A copy of the copyright notice and license.

- kunteksto.conf
    This file is the required configuration file for Kunteksto.

Directories
-----------

- example_data
    This directory contains information and sample data files for the tutorials. There is also an example of the completed Demo database, model, and data in the archive Demo_with_semantics.zip. 

- s3model
    Support files required for operation.

    - s3model.owl - the core S3Model ontology.
    - s3model_3_1_0.xsd - the reference model schema version 3.1.0
    - s3model_3_1_0.rdf - the extracted semantics from the reference model schema version 3.1.0
    - s3model_3_1_0.xsl - a stylesheet providing visualization in a browser of the reference model schema version 3.1.0
    - dm-description.xsl - a stylesheet that provides for visualization in a browser of any S3Model data model.  


.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation of the word *Context*. See `Wikipedia <https://simple.wikipedia.org/wiki/Esperanto>`_ for more information about the Esperanto language.
