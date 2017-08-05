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

Kunteksto includes a demo data file *Demo.csv*, that you can use to create your first model and data translation. This is a screenshot of the entire file as depicted in a spreadsheet. 

.. image:: _images/csv_data.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Demo.csv

Notice that there are a few columns to demonstrate various datatypes as well as one column with mixed types that might look like an integer column at first glance but has a missing value. 

This tutorial does not demonstrate all of the functionality of Kunteksto but it does demonstrate the process of creating a model based on data and then enhancing that data with improved semantics.

Kunteksto is a commandline tool that uses a combination of commandline options as well as a configuration file.
The configuration file is covered in :ref:`config`. The default configuration is fine for the tutorials.

.. _tutorsteps:


Tutorial Steps
==============

- Navigate to the directory where you installed Kunteksto.

- With the virtual environment active, start Kunteksto: 

.. code-block:: sh

    kunteksto

- At the **Enter a valid mode:** prompt, type *all*

- At the **Enter a valid CSV file:** prompt, type *example_data/Demo.csv* 

- Kunteksto will analyze the input file and create a results database of this CSV file named *output/Demo/Demo.db*  

- The output/Demo/Demo.db file should open in the SQLiteBrowser. If it does not automatically open then you will need to manually open the file with the tool you installed to open SQLite Databases. In the configuration section of these docs you will learn how to fix this issue. 

- Once the database is open use your filemanager to navigate to the *example_data* subdirectory and open the *Demo_info.pdf* file. This file simulates what often purports to be a data dictionary that you might receive with a dataset. You will use this to improve the computable semantics of your data. 

- In the SQLiteBrowser, select the *Browse Data* tab and the *model* table. Edit the title, description, copyright, author and contributor fields as desired. These fields describe the overall metadata for your data model. Basically it describes the where, when and why the data is being modeled. When you click on a field it places the contents in the larger box on the right side for easier editing. You will notice that some of this information can be obtained from the PDF. Other bits you have to just wing it based on your knowledge of the dataset. In this demo case we are going to say that we have a local ontology that describes the columns. You *MUST* use the *Apply button* to save changes when editing fields.

- This image depicts the view of the model table and below that are descriptions of each of the fields to be edited; or not. 


.. note::

    We recommend opening images in a new tab for full resolution. 

.. image:: _images/edit_model.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Edit Model


**Model table field descriptions:**

	- *title* is a free text title for your data concept contained in the CSV file.
	- *description* is a free text, elborated description of the data contained in the CSV file.
	- *copyright* enter the name of the copyright holder of the model
	- *author* enter the name of the author of the model
	- *definition_url* enter a URL (or at least a URI) to a vocabulary or ontology or a webpage that describes or defines the overall concept of the data. 

.. warning::

	- *dmid* System Generated, **Do Not Edit**
	- *entryid* System Generated, **Do Not Edit**
	- *dataid* System Generated, **Do Not Edit**  


- Select the record table. Note that there is a record for each column of data in Demo.csv. If there is only one record then the likely problem is that an incorrect field delimiter was chosen or the default was changed in the config file.  

   - each record has a number of fields that allow you to describe more about your data.
   - though some fields are pre-filled, it is only a guess and may not be accurate.
   - it is up to you to be as accurate as possible in describing your data to improve usability

.. image:: _images/record_table.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Edit Record


**Record table field descriptions:**

.. warning::

    - *header* is the column names from the data file. **Do Not Edit**.

Edit these:

    - *label* is a variation of the header text and should be edited as needed to provide a meaningful name for the column.
    - *datatype* the analyzer attempts to guess the correct datatype for the column. You must enter the correct type; string, integer, decimal or date. 
    - *min_len* enter the minimum length restriction if there is one.
    - *max_len* enter the maximum length restriction if there is one.
    - *choices* for string datatypes you may enter a set of choices to restrict the valid values. Separate each choice with a pipe '|' character.
    - *regex* for string datatypes you may enter a regular expression (XML Schema syntax) to constrain the valid string values.
    - *min_val* enter the minimum value restriction for integer or decimal columns.
    - *max_val* enter the maximum value restriction for integer or decimal columns.	
    - *vals_inclusive* are the minimum and maximum values inclusive in the valid values range. Enter a '1' for yes or a '0' for no.
    - *definition_url* enter a URL (or at least a URI) to a vocabulary or ontology or a webpage that describes or defines the meaning of the data in this column.
    - *pred_obj_list* enter any additional predicate object pairs to be used to define this resource. Enter them one per line with the predicate and object separated by a space character. You may use namespace abbreviations if they are in the list below. Otherwise you must include the full URI in order to create valid models.
    - *def_txt_value* enter the default value for a string datatype column, if there is one.
    - *def_num_value* enter the default value for a decimal or integer datatype column, if there is one.
    - *units* enter the units value for a decimal or integer datatype column. This can be an abbreviation but should come from a standard units vocabulary such as https://github.com/HajoRijgersberg/OM or http://unitsofmeasure.org/trac For integer columns where the values are *counts* you should enter the name of the item(s) being counted. This could be the same as the label or column header if desired.

.. warning::

    - *mcid* System Generated, **Do Not Edit**
    - *adid* System Generated, **Do Not Edit**  

Adding Semantics
----------------

Editing the fields in this database will improve the semantics in your model that describes the data. This allows your data consumers to make better decisions about what the data means. Kunteksto produces an executable model that can be used in various validation and knowledge discovery scenarios for your data.

In the **model** table you should change the fields as you wish to match your organization. The field *definition_url* is where we point to the overarching definition about this datamodel. This URL will be used as the *object* portion of a RDF triple where the *subject* is the unique datamodel ID (dm-{uuid}) and the *predicate* is **rdfs:isDefinedBy**. We see in our *Demo_info.pdf* file that it is declared to be found at https://www.datainsights.tech/Demo_info.pdf so this is our URL for this field.  

In the **record** table, the *definition_url* and *pred_obj_list* are where we add semantics in RDF format. The *definition_url* is formatted the same as for the *definition_url* column in the model table. 

The *pred_obj_list* column is slightly different in that you need to supply both the predicate and the object. 

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
    - sioc="http://rdfs.org/sioc/ns#"
    - sh="http://www.w3.org/ns/shacl#"
    - s3m="https://www.s3model.com/ns/s3m/"

For example, if you want to define an alternate label in addition to the label column, you could use the SKOS *skos:altLabel* predicate. However, if you want to use the predicate *isSettingFor* from the Information Objects ontology at http://www.ontologydesignpatterns.org/ont/dul/IOLite.owl then you would need to use the full URI: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#isSettingFor as the predicate. The field is an open text field so you must use care in making your entries here.  Each predicate/object pair is entered on one line with a space between the predicate and object. For example:

.. code-block:: sh

     skos:altLabel Blue Spot
     http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#isSettingFor https://www.datainsights.tech/thingies/PurpleKnob

The *object* can contain spaces. However, the first space character defines the separation between the *predicate* and *object*. 

Again, the information in the table in the PDF can help you determine additional meaning about the data if you are not a domain expert in this area of *Fake System* information. If you do not already have an ontology defining the meaning of these columns then you can search in places like http://lov.okfn.org/dataset/lov https://www.bioontology.org/ or even places that aren't formal ontologies but contain reliable definitions and descriptioins such as http://www.dictionary.com/ and https://en.wikipedia.org/wiki/Main_Page  

- Once you have completed the data description step, **saved your changes** using the *Write Changes* button in the top toolbar, close the DB Browser. You will then see that model generation happens followed by data generation. 

.. note::

    If for some reason you had to manually open the database with sqlitebrowser or another tool, then the processing will not continue automatically. Use this command to restart the model and data generation process:

    .. code-block:: sh

        kunteksto -i example_data/Demo.csv -m all -db output/Demo/Demo.db

    This tells Kunteksto to use the Demo.db and restart model and data generation with Demo.csv.



- In the *output/Demo* directory along with the Demo.db you will see an XML Schema (\*.xsd) model file and a RDF (\*.rdf) file. These are the structural and semantic models that can be used in your analysis as well as shared with others to better describe the data. The RDF file is actually extracted from the XML Schema so only the schema needs to be shared in order to distribute full structural and semantic information in an executable model. Data Insights, Inc. provides a utility with S3Model to extract the semantics from the schema data models. 

.. image:: _images/output_dir.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Output Directory

- The *all* mode causes the creation of data instances (XML, JSON and RDF) for each record in the CSV file that are semantically compliant with the RDF and will be valid according to the XML Schema. Demonstrating that the models describe the data. The RDF file does include some constraint definitions based on SHACL https://www.w3.org/TR/shacl/ However, there is no builtin processing for these constraints. Full validation is performed via XML for both the data model and data instances. In addition, an XML catalog is dynamically generated for each project and is written to the catalogs subdirectory.

- Notice that the validation file *Demo_validation_log.csv* shows four valid records and one invalid record. The invalid record is due to a 'NaN' entry in a numeric column. 

.. note::

    The S3Model eco-system has a much more sophisticated ability to handle missing and erroneous data. The details are available in the S3Model documentation.


Additional Steps
----------------

In realworld situtaions we will often be generating data on a continuing basis for this same model. To demonstrate this functionality you will use the Demo2.csv file. From the commandline issue this command: 

.. code-block:: sh

    kunteksto -i example_data/Demo2.csv -m generate -db output/Demo/Demo.db

This says to use the *Demo2.csv* file with the mode for generate and the database to reuse is the *Demo.db*. The information for the XML Schema is gathered from the information in the database and the \*.xsd file is assumed to be in the directory with the database. A new validation log is generated *Demo2_validation_log.csv* and it will have two files that are invalid. 

It is important to realize that the CSV files must represent **EXACTLY** the same type of data in order to reuse the database and schema. If you issue this on the commandline: 

.. code-block:: sh

    kunteksto -i example_data/Demo3.csv -m generate -db output/Demo/Demo.db

You will see this error message:

.. code-block:: sh

    There was an error matching the data input file to the selected model database.
    Datafile: Bad_Column_name  Model: Column_1

and no new data files were generated because the data format, in this case a column name, didn't match. 

Using this rich data
--------------------

Now that we have all these files, what can we do with them?

In the :ref:`config` section you will learn about automatically placing your data into appropriate databases/repositories for further usage. If yours is not yet supported, you an manually import from the filesystem. Of course you can also contribute, see :ref:`develop`.

In order to exploit the richness of the RDF data you will need to also load these files into your RDF repository:

- s3model/s3model.owl
- s3model/s3model_3_0_0.rdf
- output/Demo/dm-{uuid}.rdf

In your XML DB or in the appropriate place in your data pipeline you will want to use the dm-{uuid}.xsd data model schema to validate your XML data. You should be using XML Catalog files and an example is created for each project in the *catalogs* directory. 

Your JSON data instances can be used as desired on the filesystem of in a document DB. 

Why multiple copies of the same data?
-------------------------------------

You can choose which types to actually create in the :ref:`config` file. But each one has different qualities. For example the XML data is the most robust as far as any data quality validation is concerned. The RDF is more useful for exploration and knowledge discovery and the JSON is simpler to use in some environments.


More Information
----------------

- To gain a better grasp of the capability of Kunteksto, you may also want to perform the :ref:`pimatutor`. This tutorial is based on the popular Pima Indian Diabetes study that is used in many other data science tutorials. The data is realistic as opposed to this simple demo. Also, you will be actually looking up semanntics in online repositories.  


