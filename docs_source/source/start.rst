===============
Getting Started
===============

First Steps
===========

Ensure that you have the requirements and have performed the installation as described in the :ref:`install` section for your operating system. 

Then proceed to the tutorial.

.. _tutor:

Tutorial/Demo
=============

Kunteksto includes a demo data file *Demo.csv*, that you can use to create your first model and data translation. Below is a screenshot of the entire file as depicted in a spreadsheet. 

.. image:: _images/csv_data.png
    :width: 500px
    :align: center
    :height: 300px
    :alt: Demo.csv

Notice that there are a few columns to demonstrate various datatypes as well as one column with mixed types that might look like an integer column at first glance but has a missing value. 

This tutorial does not demonstrate all of the functionality of Kunteksto, but it does demonstrate the process of creating a model based on data and then enhancing that data with improved semantics.

Kunteksto is a command line tool that uses a combination of command line options as well as a configuration file.
The configuration file options are covered in :ref:`config`. The default configuration is okay for the tutorials.

.. _tutorsteps:


Tutorial Steps
==============

- Navigate to the directory where you installed Kunteksto.

- With the virtual environment active.

.. caution::

    If you closed and reopened a new window, then you need to activate the environment again. Also, be certain that you are in the kunteksto directory. 

    **Windows**

    .. code-block:: sh

        activate <path/to/directory> 

    **or Linux/MacOSX**

    .. code-block:: sh

        source activate <path/to/directory> 


.. note::

    Kunteksto can be executed in prompt mode, or several options can be provided on the command line.
    You can see all of the Kunteksto command line options using the --help flag.

    .. code-block:: sh

        kunteksto --help


For this tutorial, you start Kunteksto in prompt mode. These mandatory items will be requested:

.. code-block:: sh

    kunteksto


- At the **Enter a valid mode:** prompt, type *all*

- At the **Enter a valid CSV file:** prompt, type *example_data/Demo.csv* 

- Kunteksto analyzes the input file and creates a results database of this CSV file named *output/Demo/Demo.db*  

- The Model Metadata window opens.

- This image depicts the view of the Model Metadata and below that are descriptions of each of the fields to be edited. Kunteksto prefills the fields with fake data so that you are not staring at blank input boxes. 


.. image:: _images/edit_model.png
    :width: 500px
    :align: center
    :height: 300px
    :alt: Edit Model


**Model table field descriptions:**

    - *Title* is a free text title for your data concept contained in the CSV file.
    - *Description* is a free text, elaborated description of the data contained in the CSV file.
    - *Copyright* enter the name of the copyright holder of the model
    - *Author* enter the name of the author of the model
    - *Defining URL* enter a URL (or at least a URI) to a controlled vocabulary or ontology or a webpage that describes or defines the overall concept of the data model. 



.. note::
   
   With your file manager, navigate to the *kunteksto/example_data* subdirectory and open the *Demo_info.pdf* file. This file simulates what often purports to be a data dictionary that you might receive with a dataset. Using information from this document improves the computable semantics of your data. 


Edit these fields as desired. They describe the overall metadata for your data model. This metadata describes the where, when and why the data is useful to the model. 

Notice that some of this information can be obtained from the PDF. For other items, you have to use your knowledge of the dataset as a domain expert. In this *demo* we are going to say that we have a local ontology that describes the columns and that information is provided below in the *Adding Semantics* section below. 

.. warning::

    Use the *Save & Exit* button when you are finished making changes.


- The records editor opens next. Note that there is a record for each column of data in Demo.csv. 


.. warning::

    If there is only one record and your Label field looks like this image, then the likely problem is that an incorrect field delimiter was chosen on the command line or the default was changed in the config file. The config file should have a *comma* as the delim option, and this entry is found on or near line 9 in kunteksto.conf. 

    .. image:: _images/bad_delim.png
        :width: 400px
        :align: center
        :height: 100px
        :alt: Bad Delimiter



- Each record has some fields that allow you to describe more about your data. You can cycle through the records with the *Next* and *Previous* buttons. When you make changes, use the *Save* button to record those changes. Once the changes are written to the database, a **Saved** dialog box appears. 

.. warning::

    If you navigate away from a record without saving it, those changes are lost.

- Though some fields are pre-filled, it is only a guess and may not be accurate.

- It is up to you to be as accurate as possible in describing your data to improve quality and usability. Some fields are not used with all data types. See the description of each field below.

.. image:: _images/edit_record.png
    :width: 500px
    :align: center
    :height: 300px
    :alt: Edit Record


**Record field descriptions:**

Edit these columns (see :ref:`semantics`) :

    - *Label* was derived from the column header text and should be edited as needed to provide a more meaningful name for the column.
    
    - *Datatype* the analyzer attempts to guess the correct datatype for the column. You must select the correct type; String, Integer, Decimal, Date, Time or Datetime from the pulldown. 
    
    - *Minimum Length* for **String** columns enter the minimum length restriction if there is one.
    
    - *Maximum Length* for **String** columns enter the maximum length restriction if there is one.
    
    - *Choices* for **String** columns you may enter a set of choices to restrict the valid values. Separate each choice with a pipe '|' character.
    
    - *Regular Expression* for **String** columns you may enter a regular expression (`XML Schema syntax <http://www.xmlschemareference.com/regularExpression.html>`_) to constrain the valid string values.

        .. warning::
            The decimal separator throughout Kunteksto is a period, do not use a comma. Do not use a thousands separators.
            Also, if you mix min/max inclusive or exclusive in an illogical manner, the system takes the inclusive value and ignore the exclusive value.
    
    - *Minimum Inclusive Value* enter the minimum inclusive value restriction for **Integer or Decimal** columns.
    
    - *Maximum Inclusive Value* enter the maximum inclusive value restriction for **Integer or Decimal** columns.    
    
    - *Minimum Exclusive Value* enter the minimum exclusive value restriction for **Integer or Decimal** columns.
    
    - *Maximum Exclusive Value* enter the maximum exclusive value restriction for **Integer or Decimal** columns.   
    
    - *Description* for all columns enter a textual description that might be used for human-readable documentation.
    
    - *Defining URL* enter a URL (or at least a URI) to a controlled vocabulary or ontology or a webpage that describes or defines the meaning of the data in this column.
    
    - *Predicates & Objects* optionally enter any additional *predicate object* pairs to be used to define this resource. Enter them one per line with the predicate and object separated by a space character. 

        .. warning::
            You may use namespace abbreviations **ONLY** if they are in the list below or have been defined in the [NAMESPACES] section of the configuration file. To do otherwise generates an invalid model and be pointless.
        
        
    - *Default Text Value* for **String** columns enter the default value for a string datatype column if there is one.
    
    - *Default Numeric Value* enter the default value for a decimal or integer datatype column, if there is one.
    
    - *Units* **mandatory** units value for all **Decimal or Integer** datatype columns. For decimal columns, this should come from a standard units vocabulary such as `Ontology of units of Measure <https://github.com/HajoRijgersberg/OM>`_ or `The Unified Code for Units of Measure <http://unitsofmeasure.org>`_. For Integer columns where the values are *counts* you should enter the name of the item(s) to be counted. For example, if this number represents the number of widgets created today. Then enter "Widgets* here. 


.. _semantics:

Adding Semantics
----------------

.. note::
   
   If not already open; with your FileManager navigate to the *kunteksto/example_data* subdirectory and open the *Demo_info.pdf* file. This file simulates what often purports to be a data dictionary that you might receive with a dataset. You use this information to improve the computable semantics of your data. 


Editing the fields in this database improves the semantics in your model that describes the data. This information allows your data consumers to make better decisions about what the data means. Kunteksto produces an executable model that can be used in various validation and knowledge discovery scenarios.

In the **Model Metadata** you should change the fields as you wish to match your organization. The field *Defining URL* is where we point to the overarching definition of this datamodel. This URL is used as the *object* portion of a RDF triple where the *subject* is the unique datamodel ID (dm-{uuid}) and the *predicate* is **rdfs:isDefinedBy**. We see in our *Demo_info.pdf* file that it is declared to exist at https://www.datainsights.tech/Demo_info.pdf so this is our URL for this field.  

In the **Records Editor**, the *Defining URL* and *Predicates & Objects* are where we add semantics in RDF format. The *Defining URL* is formatted the same as for the *Defining URL* column in the Model Metadata. 

The *Predicates & Objects* column is slightly different in that you need to supply both the predicate and the object. 

.. note::

    Kunteksto defines these namespace abbreviations:

    - vc="http://www.w3.org/2007/XMLSchema-versioning"
    - xsi="http://www.w3.org/2001/XMLSchema-instance"
    - rdfs="http://www.w3.org/2000/01/rdf-schema#"
    - rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    - owl="http://www.w3.org/2002/07/owl#"
    - xs="http://www.w3.org/2001/XMLSchema"
    - xsd="http://www.w3.org/2001/XMLSchema#"
    - dc="http://purl.org/dc/elements/1.1/"
    - dct="http://purl.org/dc/terms/"
    - skos="http://www.w3.org/2004/02/skos/core#"
    - foaf="http://xmlns.com/foaf/0.1/"
    - schema="http://schema.org/"
    - sioc="http://rdfs.org/sioc/ns#"
    - sh="http://www.w3.org/ns/shacl#"
    - s3m="https://www.s3model.com/ns/s3m/"

For example, if you want to define an alternate label in addition to the Label field, you could use the SKOS *skos:altLabel* predicate. However, if you want to use the predicate *isSettingFor* from the `Information Objects ontology <http://www.ontologydesignpatterns.org/ont/dul/IOLite.owl>`_ then you would need to first define an abbreviation for this ontology in the [NAMESPACES] section of the configuration file. You may do this while editing the database. Just be sure to save the new configuration before closing the database editor so that your changes are saved before the model generator runs. 

.. warning::

    The field is an open text field so you must use care in making your entries here.  Each predicate/object pair is entered on one line with a space between the predicate and object. For example:

.. code-block:: sh

     skos:altLabel Blue Spot
     dul:isSettingFor https://www.datainsights.tech/thingies/PurpleKnob

The *object* portion can contain spaces. However, the first space character defines the separation between the *predicate* and *object*. 

Again, the information in the table in the PDF can help you determine additional meaning about the data if you are not a domain expert in this area of *Fake System* information. If you do not already have an ontology defining the meaning of these columns then you can search in places like `BARTOC <http://www.bartoc.org/>`_, `Linked Open Vocabularies <http://lov.okfn.org/dataset/lov>`_  `Biontology <https://www.bioontology.org/>`_  or even places that aren't formal ontologies but contain reliable definitions and descriptions such as `a dictionary <http://www.dictionary.com/>`_ or an `encyclopedia <https://en.wikipedia.org/wiki/Main_Page>`_.  

- Once you have completed the data description step, **saved any changes to the configuration file** and **saved your changes** using the *Save* button on each Record, close the Record Editor with the *Exit* button. This action starts the model generation process, followed by the data generation process. 

- In the *output/Demo* directory along with the Demo.db, you find an XML Schema (\*.xsd) model file and a RDF (\*.rdf) file. These are the structural and semantic models that can be used in your analysis as well as shared with others to describe the data better. The RDF file is extracted from the XML Schema, so only the schema needs to be shared to distribute full structural and semantic information in an executable model. Data Insights, Inc. provides a utility with S3Model to extract the semantics from the schema data models. 

.. image:: _images/output_dir.png
    :width: 500px
    :align: center
    :height: 300px
    :alt: Output Directory

- The *all* mode causes the creation of data instances (XML, JSON, and RDF) for each record in the CSV file that is semantically compliant with the RDF and is valid according to the XML Schema. This validation process demonstrates that the models describe the data. The RDF file does include some constraint definitions based on `Shapes Constraint Language (SHACL) <https://www.w3.org/TR/shacl/>`_ There is no built-in processing for these constraints due to the lack of maturity of this technology. Expect SHACL to become more useful soon. 

Full validation is performed via XML for both the data model and data instances. Also, an XML catalog is dynamically generated for each project and is written to the catalogs subdirectory.

- Notice that the validation file *Demo_validation_log.csv* shows four valid records and one invalid record. The invalid record is due to a 'NaN' entry in a numeric column. 

.. note::

    The S3Model eco-system has a much more sophisticated ability to handle missing and erroneous data. The details are available in the S3Model documentation. To use this expanded exceptional value tagging generally requires the model first approach whereas Kunteksto is an after-the-fact bridge.


.. caution::
    You can rerun this Demo with different options as many times as you wish.  However, this creates a new data model each time. You should delete the *Demo* directory under the *kunteksto/output/* directory before restarting. 


Additional Steps
----------------

In real-world situations, we often generate data on a continuing basis for this same model. To demonstrate this functionality, use the Demo2.csv file. From the command line issue this command: 

.. code-block:: sh

    kunteksto -i example_data/Demo2.csv -m generate -db output/Demo/Demo.db

This command entry says to use the *Demo2.csv* file with the mode passed as *generate* and the database to reuse is the *Demo.db*. The information for the XML Schema is gathered from the information in the database, and the \*.xsd file is assumed to be in the directory with the database. A new validation log is generated *Demo2_validation_log.csv* and two files are shown as invalid. 

It is important to realize that the CSV files must represent **EXACTLY** the same type of data to reuse the database and schema. If you issue this on the command line: 

.. code-block:: sh

    kunteksto -i example_data/Demo3.csv -m generate -db output/Demo/Demo.db

You will see this error message:

.. code-block:: sh

    There was an error matching the data input file to the selected model database.
    Datafile: Bad_Column_name  Model: Column_1

also, no new data files were generated because the data format, in this case, a column name, didn't match. 

Using this rich data
====================

Now that we have all these files, what can we do with them?

In the :ref:`config` section you learn about automatically placing your data into appropriate databases/repositories for further usage. If yours is not yet supported, you can manually import from the filesystem. Of course, you can also contribute, see :ref:`develop`.

To exploit the richness of the RDF data, you load these files into your RDF repository:

- s3model/s3model.owl
- s3model/s3model_3_0_0.rdf
- output/Demo/dm-{uuid}.rdf

In your XML DB or the appropriate place in your data pipeline, you will want to use the dm-{uuid}.xsd data model schema to validate your XML data. You should be using XML Catalog files, and an example is created for each project in the *catalogs* directory. 

Your JSON data instances can be used as desired on the filesystem or in a document DB. 

There is a growing effort to expand the current data science algorithms to exploit richer data formats such as RDF. 
Some references to get you started:

- `Towards Analytics on Top of Big RDF Data <https://www.youtube.com/watch?v=VoEEb_oGN7w>`_ (video).
- `Linked Data meets Data Science <https://ablvienna.wordpress.com/2014/10/28/linked-data-meets-data-science/>`_
- `RDF on KDNuggets <http://www.kdnuggets.com/tag/rdf>`_
- `RDF on Data Science Central <http://www.datasciencecentral.com/profiles/blog/list?tag=RDF>`_


Why multiple copies of the same data?
-------------------------------------

You can choose which types to create in the :ref:`config` file. However, each one has different qualities. For example, the XML data is the most robust as far as any data quality validation is concerned. The RDF is more useful for exploration and knowledge discovery, and the JSON is simpler to use in some environments.


More Information
----------------

- To gain a better grasp of the capability of Kunteksto, you may also want to perform the :ref:`advtutor`. These tutorial demonstrate the power of S3Model using persistent storage. 


