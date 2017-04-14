"""
Main entry point for the Kunteksto application.
"""
import sys
import os
from subprocess import run
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import configparser

from analyze import analyze
from generate import makeModel, makeData

class Translate(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.seps = [',',';',':','|','$']
        self.fmts = ['XML', 'JSON']
        self.sep_type = tk.StringVar()
        self.datafmt = tk.StringVar()
        self.infile = '(none selected)'
        self.outDB = ''
        self.model = tk.StringVar()
        self.parent = parent
        self.analyzeLevel = tk.StringVar()  

        # Setup config info
        config = configparser.ConfigParser()
        config.read('kunteksto.conf')
        self.sqlbrow = config['SQLITEBROWSER']['path']
        
        self.neo4j_activate = config['NEO4J']['activate']
        self.neo4j_user = config['NEO4J']['user']
        self.neo4j_pw = config['NEO4J']['pw']
        self.neo4j_host = config['NEO4J']['host']
        self.neo4j_port = config['NEO4J']['port']
        self.neo4j_dbpath = config['NEO4J']['dbpath']
        
        self.analyzeLevel.set(config['KUNTEKSTO']['analyzeLevel'])
        self.outdir = config['KUNTEKSTO']['outDir']
        self.sep_type.set(config['KUNTEKSTO']['sepType'])
        self.datafmt.set(config['KUNTEKSTO']['datafmt'])

        self.init_gui()

    def init_gui(self):
        self.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.parent.title("Kunteksto")

        ttk.Label(self, text="Kunteksto by Data Insights, Inc.").grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text="CSV separator: ").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(self, values=self.seps, textvariable=self.sep_type, justify="center", width=1, state='readonly').grid(row=1, column=10, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Select Input CSV", command=self.opencsv).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text=self.infile).grid(row=2, column=10, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self, text="Output format: ").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(self, values=('XML', 'JSON'), textvariable=self.datafmt, justify="center", width=4, state='readonly').grid(row=3, column=10, padx=5, pady=5, sticky=tk.W)

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
        print('\nStopped Kunteksto ...\n\n')
        quit()

    def opencsv(self):
        self.infile = filedialog.askopenfilename()
        ttk.Label(self, text=self.infile).grid(row=2, column=10, padx=5, pady=5, sticky=tk.W)
        return

    def doanalyze(self):
        if self.infile:
            pbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate')
            self.outDB = analyze(self.infile, self.sep_type.get(), self.analyzeLevel.get(), pbar, self.outdir)
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
            #  self.outdir = filedialog.askdirectory(title="Select Output Directory")
            ttk.Label(self, text=self.outdir).grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        else:
            print('You must first select an input file.')

        return

    def modelgen(self):
        # generate the model
        if self.outDB and not self.outdir == '(none selected)':
            modelName = makeModel(self.outDB, self.outdir)
            self.model.set(modelName)
        else:
            print('No DB file or no selected output directory.')

        return

    def editdb(self):
        if self.outDB:
            run([self.sqlbrow,  self.outDB])
        return

    def datagen(self):
        # generate the data
        if self.model.get() and not self.outdir == '(none selected)':
            makeData(self.model.get(), self.datafmt.get(), self.outDB, self.infile, self.sep_type.get(), self.outdir)
        else:
            print('No model or no selected output directory.')

        return

if __name__ == '__main__':
    print('\nRunning Kunteksto ...\n\n')
    root = tk.Tk()
    root.geometry("600x400")
    Translate(parent=root)
    root.mainloop()
