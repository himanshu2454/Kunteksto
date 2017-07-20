===============
Getting Started
===============

First Steps
===========

Ensure that you have the requirements and have performed the installation as described in the :ref:`install` section for your operating system. 

Then proceed to the tutorial.

.. _tutor:

Tutorial
========

Kunteksto includes a demo data file that you can use to create your first model and data translation. This is a screenshot of the entire file as dipicted in a spreadsheet. 

.. image:: _images/csv_data.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Demo.csv

Notice that there are a few columns to demonstrate various datatypes as well as one column with mixed types that might look like an interger column at first glance. 

This tutorial does not demonstrate all of the functionality of the Kunteksto but it does demonstrate the process of creating a model based on data and then enhancing that data with improved semantics.

Kunteksto is a commandline tool that uses a combination of commandline options as well as a configuration file.
The configuration file is covered in another section. The default configuration is fine for the tutorials.

.. _tutorsteps:


Tutorial Steps
--------------

- Navigate to the directory where you installed Kunteksto.

- Start Kunteksto: python3 kunteksto.py

- At the **mode** prompt, type *all*

- At the **infile** propmt, type **example_data/Demo.csv** 

- Kunteksto will analyze the input file and create a results database of this CSV file named example_data/Demo.db  

- The output/Demo.db file should open in the SQLite Browser if it does not automatically open then you will need to manually open the file. In the configuration section of these docs you will learn how to fix this issue. 

- Select the *Browse Data* tab and the *model* table. Edit the title, description, copyright, author and contributor fields as desired. These fields describe the overall metadata for your data model. Basically it describes the where, when and why the data is being modeled. When you click on a field it places the contents in the larger box on the right side for easier editing.

.. image:: _images/edit_model.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Edit Model


Field descriptions:

	- *title* is a free text title for your data concept contained in the CSV file.
	- *description* is a free text, elborated description of the data contained in the CSV file.
	- *copyright* enter the name of the copyright holder of the model
	- *author* enter the name of the author of the model
	- *definition_url* enter a URL (or at least a URI) to a vocabulary or ontology or a webpage that describes or defines the overall concept of the data. 
	- *dmid* System Generated, **Do Not Edit**
	- *entryid* System Generated, **Do Not Edit**
	- *dataid* System Generated, **Do Not Edit**  


- Select the record table. Note that there is a record for each column of data in Demo.csv. If there is only one record then the likely problem is that an incorrect field delimiter was chosen or the default was changed in the config file.  

   - each record has a number of fields that allow you to describe more about your data.
   - though each field is pre-filled it is only a guess and may not be accurate.
   - it is up to you to be as accurate as possible in describing your data to improve usability

.. image:: _images/record_table.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Edit Record


Field descriptions:

    - *header* is the column names from the data file. **Do Not Edit**.
    - *label* is a copy of the header text and should be edited as needed to provide a meaningful name for the column.
    - *datatype* the analyzer attempts to guess the correct datatype for the column. You must enter the correct type; string, integer, float or date. 
    - *min_len* enter the minimum length restriction if there is one.
    - *max_len* enter the maximum length restriction if there is one.
    - *choices* for string datatypes you may enter a set of choices to restrict the valid values. Separate each choice with a pipe '|' character.
    - *regex* for string datatypes you may enter a regular expression (XML Schema syntax) to constrain the valid string values.
    - *min_val* enter the minimum value restriction for integer or float columns.
    - *max_val* enter the maximum value restriction for integer or float columns.	
    - *vals_inclusive* are the minimum and maximum values inclusive in the valid values range. Enter a '1' for yes or a '0' for no.
    - *definition_url* enter a URL (or at least a URI) to a vocabulary or ontology or a webpage that describes or defines the meaning of the data in this column.
    - *pred_obj_list* enter any additional predicate object pairs to be used to define this resource. Enter them one per line with the predicate and object separated by a space character. You may use namespace abbreviations if they are in the list below. Otherwise you must include the full URI in order to create valid models.
    - *def_txt_value* enter the default value for a string datatype column, if there is one.
    - *def_num_value* enter the default value for a float or integer datatype column, if there is one.
    - *units* enter the units value for a float or integer datatype column. This can be an abbreviation but should come from a standard units vocabulary such as https://github.com/HajoRijgersberg/OM or http://unitsofmeasure.org/trac For integer columns where the values are *counts* you should enter the name of the item(s) being counted. This could be the same as the lable or column header if desired.
    - *mcid* System Generated, **Do Not Edit**
    - *adid* System Generated, **Do Not Edit**  

- Once you have completed the data description step, saved your changes and closed the DB Browser. You will find an XML Schema model file and an RDF file in the output directory. These are the structural and semantic models that can be used in your analysis as well as shared with others to better describe the data.

.. image:: _images/output_dir.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: Output Directory

9. Now click the Generate Data button and Kunteksto will create data instances for each record in the CSV file that are semantically compliant with the RDF and will be valid according to the XML Schema. Demonstrating that the models describe the data. 



.. rubric:: Footnotes

.. [#f1] Namespace abbreviaions list:

    - 'xs':'http://www.w3.org/2001/XMLSchema',
    - 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
    - 'xsd':'http://www.w3.org/2001/XMLSchema#',
    - 'dc':'http://purl.org/dc/elements/1.1/',
    - 'skos':'http://www.w3.org/2004/02/skos/core#',
    - 'foaf':'http://xmlns.com/foaf/0.1/',
    - 'sioc':'http://rdfs.org/sioc/ns#',
    - 'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    - 'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
    - 'dct':'http://purl.org/dc/terms/',
    - 'owl':'http://www.w3.org/2002/07/owl#',
    - 'vc':'http://www.w3.org/2007/XMLSchema-versioning',
    - 's3m':'https://www.s3model.com/ns/s3m/'






