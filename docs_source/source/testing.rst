==================
Examples & Testing
==================

Kunteksto does not *currently* include Python code testing.

However, there is a test CSV file (test_gen.csv) in the example_Data directory.

This CSV file can be used to test all of the available components as well as validation issues. 

All of your models and components are stored in a database *kunteksto.db* in the Kunteksto working directory. 
You can backup this file to be usre you do not loose any work. You can always delete the database, restart Kunteksto and it will generate a new blank database. You can copy a backup into the directory to recover a previous version.

In the *example_dbs* directory there are two databases. 

- Demo_kunteksto.db 
    This database contains a  **Demo** model and completed set of components based on the tutorial. 

- TestAndDemo_kunteksto.db     
    This database contains the **Demo**as well as a **TestDB** model and completed components generated from from the test_gen.csv. 
    
By generating, exporting and validating the models and instances using external tools such as Xerces or Saxon you can verify the validity of Kunteksto models and data instances.

