"""
analyze.py

This is the database layout. See the documentation for details on each field.

model table: 
0 - title = CHAR(250)
1 - description = TEXT
2 - copyright = CHAR(250)
3 - author = CHAR(250)
4 - definition_url = CHAR(500)
5 - dmid = CHAR(40)
6 - entryid = CHAR(40)
7 - dataid = CHAR(40)

record table:
 0 - header = char(100)
 1 - label = char(250)
 2 - datatype = char(10)
 3 - min_len = int
 4 - max_len = int
 5 - choices = TEXT
 6 - regex = CHAR(250)
 7 - min_val = FLOAT
 8 - max_val = FLOAT
 9 - vals_Inclusive = BOOL
10 - definition_url = CHAR(500)
11 - pred_obj_list = TEXT
12 - def_txt_value = TEXT
13 - def_num_value = FLOAT
14 - units = CHAR(50)
15 - mcid = CHAR(40)
16 - adid = CHAR(40)

"""
import sys
import os
import time
import csv
import sqlite3

from uuid import uuid4
from collections import OrderedDict
import iso8601
import configparser
import argparse
from subprocess import run

def analyze(csvInput, delim, level, out_dir):
    """
    Load and analyze the CSV file.
    Create a database used to describe the data.
    """

    dname, fname = os.path.split(csvInput)
    dbName = fname[:fname.index('.')] + '.db'
    db_file = out_dir + os.path.sep + dbName
    
    # if this database already exists then delete it
    try:
        os.remove(db_file)
    except OSError:
        pass

    # create the database with the two tables.
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE "model" ("title" CHAR(250), "description" TEXT, "copyright" CHAR(250), "author" CHAR(250), "definition_url" CHAR(500), "dmid" CHAR(40), "entryid" CHAR(40), "dataid" CHAR(40))""")
    c.execute("""CREATE TABLE "record"  (header  char(100), label char(250), datatype char(10), min_len int, max_len int, "choices" TEXT, "regex" CHAR(250), "min_val" FLOAT, "max_val" FLOAT, "vals_Inclusive" BOOL, "definition_url" CHAR(500), "pred_obj_list" TEXT, "def_txt_value" TEXT, "def_num_value" FLOAT, "units" CHAR(50), "mcid" CHAR(40), "adid" CHAR(40))""")

    # create the initial data for the record table.
    data = []
    with open(csvInput) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delim)
        for h in reader.fieldnames:
            mcID = str(uuid4())  # model component
            adID = str(uuid4())   # adapter
            label = 'The ' + h.replace('_', ' ')
            data.append((h, label, 'String', None, None, '', '',
                         None, None, True, '', '', '', None, '', mcID, adID))

    c = conn.cursor()
    c.executemany(
        "INSERT INTO record VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()

    # create the initail data for the model table
    dmID = str(uuid4())   # data model
    entryID = str(uuid4())   # entry
    dataID = str(uuid4())   # data cluster

    data = [('S3M Data Model', 'S3M Data Model for ' + csvInput, 'Copyright 2017, Data Insights, Inc.',
             'Data Insights, Inc.', 'http://www.some_url.com', dmID, entryID, dataID)]
    c.executemany("insert into model values (?,?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()

    if level == 'Full':
        conn = sqlite3.connect(db_file)
        # indepth analysis of columns for datatypes and ranges.
        with open(csvInput) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delim)
            hdrs = reader.fieldnames
            dataDict = OrderedDict()
            for h in reader.fieldnames:
                dataDict[h] = []

            for row in reader:
                for h in reader.fieldnames:
                    dataDict[h].append(row[h])

        # pbar.grid(row=8, column=10, padx=5, pady=5, sticky=tk.W)
        hdrs = dataDict.keys()

        typedict = {}
        for h in hdrs:
            # test each data item from a column. if one is not a type, turn off that type.
            dlist = dataDict[h]
            is_int = False
            is_float = False
            is_date = False
            is_str = False
            maxval = None
            minval = None

            for x in dlist:
                try:
                    int(x)
                    is_int = True
                except:
                    is_int = False
                    break

            for x in dlist:
                try:
                    if not is_int:
                        float(x)
                        is_float = True
                except:
                    is_float = False
                    break

            for x in dlist:
                try:
                    if not is_int and not is_float:
                        iso8601.parse_date(x)
                        is_date = True
                except:
                    is_date = False
                    break

            for x in dlist:
                try:
                    if not is_int and not is_float and not is_date:
                        str(x)
                        is_str = True
                except:
                    is_str = False
                    break

            if is_int:
                intlist = [int(x) for x in dlist]
                maxval = max(intlist)
                minval = min(intlist)
            if is_float:
                flist = [float(x) for x in dlist]
                maxval = max(flist)
                minval = min(flist)

            if is_int:
                dt = "Integer"
            elif is_float:
                dt = "Float"
            elif is_date:
                dt = "Date"
            else:
                dt = "String"

            # edit the database record for the correct type
            c = conn.cursor()
            c.execute(
                """UPDATE record SET datatype = ?, max_val = ?, min_val = ? WHERE header = ? """, (dt, maxval, minval, h))
            conn.commit()

        conn.close()

    return(db_file)


if __name__ == '__main__':
    os.environ['XML_CATALOG_FILES'] = 'Kunteksto_catalog.xml'
    print('\n Kunteksto analyze is running ...\n\n')
    # Setup config info
    config = configparser.ConfigParser()
    config.read('kunteksto.conf')
    delim = config['KUNTEKSTO']['sepType']
    level = config['KUNTEKSTO']['analyzeLevel']
    
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str, help="The input CSV file to analyze.")
    parser.add_argument("out", type=str, help="The output directory to store the database, models and data. Do not include a trailing slash.")
    parser.description = "The CSV must be readable and the ouput dir be writable by the user executing this program."
    args = parser.parse_args()
    if args.csv:
        csvInput = args.csv
    else:
        print("\nCSV Input is required.\n")
        exit()

    if args.out:
        out_dir = args.out
    else:
        print("\nOutput directory is required.\n")
        exit()

    dbFile = analyze(csvInput, delim, level, out_dir)
    
    print("Created: " + dbFile)
    
    run([config['SQLITEBROWSER']['cmd'], dbFile])
    
    print("\n Now generate your models and data with the Kunteksto generator.\n")
    exit(code=0)
    