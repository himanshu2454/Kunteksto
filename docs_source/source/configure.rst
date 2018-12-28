=============
Configuration
=============

.. warning::

    Only edit the configuration file with a text editor. Do not use a word processing application such as MS Word or LibreOffice. There are many great opensource and free text editors from which to choose.  Some favorites, in no particular order, are:

    - `Atom <https://atom.io/>`_
    - `VS Code <https://code.visualstudio.com/>`_
    - `Sublime <https://www.sublimetext.com/>`_

The initial kunteksto.conf file should be okay for most uses and indeed for this initial tutorial. You are encouraged to make backup copies, under different names, of the configuration file for different use cases/projects. The active configuration, however, is always the one named **kunteksto.conf**. Kunteksto ships with a copy of the original config file named *default.conf* as well as a config file for the advanced tutorials named *advanced_tutorials.conf*. You can always go back to the initial settings by making a copy of the *default.conf* file and naming it *kunteksto.conf*.

.. _config:

Config File Details
===================
Here we cover the details of the configuration options. 


.. sourcecode:: text

    [KUNTEKSTO]
    ; check the documentation for a list of themes
    ; theme demos are here https://bootswatch.com/3/cosmo/
    theme: sandstone

    ; The default data (CSV) file delimiter is defined here. 
    ; allowed delimiter (field separator) types are one of these:  , ; : | $ 
    ; A different delimiter may be passed on the commandline that will override this one.
    delim: ,


**There are no options editable by the user in the SYSTEM section.**

.. sourcecode:: text


    [SYSTEM]
    version: 2.0.0  
    rmversion: 3.1.0

The *version* is the current version of Kunteksto.
The *rmversion* is the version of the S3Model Reference Model that is used for generated data models and RDF. 
