"""
Main entry point for the Kunteksto application.
"""
import sys
import os
from subprocess import run
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import configparser

from analyze import analyze
from generate import makeModel, makeData

class Translate(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.seps = [',',';',':','|','$']
        self.sep_type = tk.StringVar()
        self.infile = '(none selected)'
        self.outDB = ''
        self.model = tk.StringVar()
        self.parent = parent
        self.analyzeLevel = tk.StringVar()  

        # Setup config info
        config = configparser.ConfigParser()
        config.read('kunteksto.conf')
        self.sqlbrow = config['SQLITEBROWSER']['path']
        # get the RDF Store parameters.
        self.agraphStatus = config['ALLEGROGRAPH']['status']
        self.agraphHost = config['ALLEGROGRAPH']['host']
        self.agraphPort = config['ALLEGROGRAPH']['port']
        self.agraphRepo = config['ALLEGROGRAPH']['repo']
        self.agraphUser = config['ALLEGROGRAPH']['user']
        self.agraphPW = config['ALLEGROGRAPH']['pw']
        
        self.stardogStatus = config['STARDOG']['status']

        self.blazegraphStatus = config['BLAZEGRAPH']['status']

        self.graphdbStatus = config['GRAPHDB']['status']

        # get the XML DB parameters.
        self.basexStatus = config['BASEX']['status']
        self.basexHost = config['BASEX']['host']
        self.basexPort = config['BASEX']['port']
        self.basexDBName = config['BASEX']['dbname']
        self.basexUser = config['BASEX']['user']
        self.basexPW = config['BASEX']['pw']

        self.exisdbStatus = config['EXISTDB']['status']

        # get the JSON DB parameters.
        self.mongoStatus = config['MONGODB']['status']
        self.mongoHost = config['MONGODB']['host']
        self.mongoPort = config['MONGODB']['port']
        self.mongoDBName = config['MONGODB']['dbname']
        self.mongoUser = config['MONGODB']['user']
        self.mongoPW = config['MONGODB']['pw']

        self.couchStatus = config['COUCHDB']['status']

        self.analyzeLevel.set(config['KUNTEKSTO']['analyzeLevel'])
        self.outdir = config['KUNTEKSTO']['outDir']
        self.sep_type.set(config['KUNTEKSTO']['sepType'])
        self.init_gui()

    def init_gui(self):
        self.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.parent.title("Kunteksto")

        ttk.Label(self, text="Kunteksto by Data Insights, Inc.").grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text="CSV separator: ").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(self, values=self.seps, textvariable=self.sep_type, justify="center", width=1, state='readonly').grid(row=1, column=10, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Select Input CSV", command=self.opencsv).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text=self.infile).grid(row=2, column=10, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Select Output Directory", command=self.outputsel).grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self, text=self.outdir).grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
 
        ttk.Button(self, text="Analyze CSV", command=self.doanalyze).grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Checkbutton(self, text='Full Analysis', variable=self.analyzeLevel, onvalue='Full', offvalue='Simple').grid(row=6, column=10, padx=5, pady=5, sticky=tk.W)
        self.msgAnalyze = tk.StringVar()
        self.msgAnalyze.set('')
        ttk.Label(self, textvariable=self.msgAnalyze).grid(row=7, column=10, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Generate Model", command=self.modelgen).grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self, text="Re-Edit Database", command=self.editdb).grid(row=9, column=10, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, textvariable=self.model).grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Generate Data", command=self.datagen).grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Quit", command=self.on_quit).grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)


    def on_quit(self):
        quit()

    def opencsv(self):
        self.infile = filedialog.askopenfilename()
        ttk.Label(self, text=self.infile).grid(row=2, column=10, padx=5, pady=5, sticky=tk.W)
        return

    def doanalyze(self):
        if self.infile:
            pbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate')
            self.outDB = analyze(self.infile, self.sep_type.get(), self.analyzeLevel.get(), pbar, self.outdir)
            if self.outDB:
                self.msgAnalyze.set('Created: ' + self.outDB)
                run([self.sqlbrow,  self.outDB])
        return

    def outputsel(self):
        if self.infile:
            dir_opt = {}
            dir_opt['initialdir'] = './output'
            dir_opt['mustexist'] = True
            dir_opt['parent'] = self
            dir_opt['title'] = 'Select a data output directory'
            self.outdir = filedialog.askdirectory(**dir_opt)        
            ttk.Label(self, text=self.outdir).grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        else:
            messagebox.showerror('Procedure Error','You must first select an input file.')

        return

    def modelgen(self):
        # generate the model
        if self.outDB and not self.outdir == '(none selected)':
            modelName = makeModel(self.outDB, self.outdir)
            self.model.set(modelName)
        else:
            messagebox.showerror('Procedure Error','Missing DB file or no selected output directory.')

        return

    def editdb(self):
        if self.outDB:
            run([self.sqlbrow,  self.outDB])
        return

    def datagen(self):
        # open a connection to the RDF store if one is defined. 
        if self.agraphStatus == "ACTIVE":
            from franz.openrdf.connect import ag_connect
            connRDF = ag_connect(self.agraphRepo, host=self.agraphHost, port=self.agraphPort,  user=self.agraphUser, password=self.agraphPW)
            print(connRDF.size())
        else:
            connRDF = None

        # open a connection to the XML DB if one is defined. 
        if self.basexStatus == "ACTIVE":
            import BaseXClient
            connXML = BaseXClient.Session(self.basexHost, int(self.basexPort), self.basexUser, self.basexPW)
            connXML.execute("create db " + self.basexDBName)
        else:
            connXML = None
            
        # open a connection to the JSON DB if one is defined. 
        if self.mongoStatus == "ACTIVE":
            from pymongo import MongoClient
            client = MongoClient(self.mongoHost, int(self.mongoPort))  # default MongoDB has no authentication requirements.
            connJSON = client[self.mongoDBName]
        else:
            connJSON = None
            
            
        # generate the data
        if self.model.get() and not self.outdir == '(none selected)':
            makeData(self.model.get(), self.outDB, self.infile, self.sep_type.get(), self.outdir, connRDF, connXML, connJSON)
            
            if connRDF:
                connRDF.close()
            if connXML:
                connXML.close()
                
                
        else:
            messagebox.showerror('Procedure Error','Missing model or no selected output directory.')

        return

if __name__ == '__main__':
    print('\n Kunteksto is running ...\n\n')
    root = tk.Tk()
    root.geometry("600x400")
    Translate(parent=root)
    root.mainloop()
