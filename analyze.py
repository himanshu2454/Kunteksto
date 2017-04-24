"""
analyze.py

"""
import sys
import os
import time
import csv
import sqlite3
import tkinter as tk
from tkinter import messagebox

from uuid import uuid4
from collections import OrderedDict
import iso8601

def analyze(csvInput, delim, level, pbar, out_dir):
    """
    Load and analyze the CSV file.
    Create a database used to describe the data.
    """
    if csvInput == '(none selected)':
        messagebox.showerror('Procedure Error', 'CSV Selected: ' + csvInput)
        return None
    
    pbar.start()

    dname, fname = os.path.split(csvInput) 
    dbName = fname[:fname.index('.')] + '.db'
    db_file = out_dir + os.path.sep + dbName
    
    try:
        os.remove(db_file)
    except OSError:
        pass

    # create the base database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE "model" ("title" CHAR(250), "description" TEXT, "copyright" CHAR(250), "author" CHAR(250), "definition_url" CHAR(500), "dmid" CHAR(40), "entryid" CHAR(40), "dataid" CHAR(40))""")
    c.execute("""CREATE TABLE "record"  (header  char(100), label char(250), datatype char(10), min_len int, max_len int, "choices" TEXT, "regex" CHAR(250), "min_val" FLOAT, "max_val" FLOAT, "vals_Inclusive" BOOL, "definition_url" CHAR(500), "def_txt_value" TEXT, "def_num_value" FLOAT, "units" CHAR(50), "mcid" CHAR(40), "adid" CHAR(40))""")

    data = []
    with open(csvInput) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delim)
        for h in reader.fieldnames:
            mcID = str(uuid4())  # model component
            adID = str(uuid4())   # adapter
            label = 'The ' + h.replace('_', ' ')
            data.append((h,label,'String',None,None,'','',None,None,True,'','',None,'', mcID, adID))

    c = conn.cursor()
    c.executemany("INSERT INTO record VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()
    dmID = str(uuid4())   # data model
    entryID = str(uuid4())   # entry
    dataID = str(uuid4())   # data cluster

    data =[ ('S3M Data Model','S3M Data Model for ' + csvInput,'Copyright 2017, Data Insights, Inc.','Data Insights, Inc.', 'http://www.some_url.com', dmID, entryID, dataID)]
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
        pbar['value'] = 0
        pbar['maximum'] = len(hdrs)

        typedict = {}
        for h in hdrs:
            pbar['value'] += 1
            dlist = dataDict[h]  # test each data item from a column. if one is not a type, turn off that type.
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
            c.execute("""UPDATE record SET datatype = ?, max_val = ?, min_val = ? WHERE header = ? """, (dt, maxval, minval, h))
            conn.commit()

        conn.close()


    return(db_file)
