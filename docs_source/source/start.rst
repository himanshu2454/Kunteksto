===============
Getting Started
===============

First Steps
===========

Ensure that you have the requirements and have performed the installation as described for your operating systems. 


Tutorial
========

Kunteksto includes a demo data file that you can use to create your first model and data translation. 

This does not include all of the functionality of the data translator but it does demonstrate the process. 

The first step is to analyze the data file. Data files must plain text (often called CSV) files that have each record on a row, seperated by a CR/LF and each field in the record delimited by a separator.  
The allowed spearators are:

- comma : ","
- semi-colon : ";"
- colon : ":"
- pipe : "|"
- dollar sign : "$"

The first row of the data file MUST contain column names. See the documentation on semantics and best practices for naming. 

Tutorial Steps
--------------

1. Start Kunteksto: python3 kunteksto.py
2. Select the semi-colon separator using the select box (Demo.csv uses a semicolon ';' for the field separator).
3. Select the demo file, Demo.csv using the open file dialog.
4. Kunteksto will create a results database of this CSV file named Demo.db when the Analyze CSV button is clicked. 
5. Open the Demo.db file using the DB Browser for SQLite if it does not automatically open. 
6. Select the model table and edit the title, description, copyright, author and contributor fields as desired. These fields describe the overall metadata for your data model.
7. Select the record table. Note that there is a record for each column of data in Demo.csv. If there is only one record then the likely problem is that an incorrect separator was chosen.  

   - each record has a number of fields that allow you to describe more about your data.
   - though each field is pre-filled it is only a guess and may not be accurate.
   - it is up to you to be as accurate as possible in describing your data to improve reusability

8. Once you have completed the data description step, select the data format you want using the combobox and select an output directory.
9. Click the Create Output button. You will find an XML Schema model file in the directory as well as two subdirectories. These two subdirectories contain your converted data (data) in XML or JSON and the semantics graph (rdf).


