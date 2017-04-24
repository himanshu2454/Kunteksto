"""
generate.py
"""
import sys
import os
import time
import datetime
import csv
import sqlite3
import tkinter as tk
from uuid import uuid4
from collections import OrderedDict
from lxml import etree
import json
import xmltodict
import shortuuid
import iso8601
from tkinter import messagebox

def xsdHeader():
    """
    Build the header string for the XSD
    """
    hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
    hstr += '<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>\n'
    hstr += '<xs:schema\n'
    hstr += '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
    hstr += '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    hstr += '  xmlns:owl="http://www.w3.org/2002/07/owl#"\n'
    hstr += '  xmlns:xs="http://www.w3.org/2001/XMLSchema"\n'
    hstr += '  xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
    hstr += '  xmlns:sawsdlrdf="http://www.w3.org/ns/sawsdl#"\n'
    hstr += '  xmlns:sch="http://purl.oclc.org/dsdl/schematron"\n'
    hstr += '  xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"\n'
    hstr += '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    hstr += '  xmlns:skos="http://www.w3.org/2004/02/skos/core#"\n'
    hstr += '  xmlns:s3m="http://www.s3model.com/ns/s3m/"\n'
    hstr += '  targetNamespace="http://www.s3model.com/ns/s3m/"\n'
    hstr += '  vc:minVersion="1.1" xml:lang="en-US">\n\n'
    hstr += '  <xs:include schemaLocation="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd"/>\n\n'
    return(hstr)

def xsdMetadata(md):
    mds = '<!-- Metadata -->\n  <xs:annotation><xs:appinfo><rdf:RDF><rdf:Description\n'
    mds += '    rdf:about="' + md[0] + '">\n'
    mds += '    <dc:title>' + md[1].strip() + '</dc:title>\n'
    mds += '    <dc:creator>' + md[2] + '</dc:creator>\n'
    mds += '    <dc:contributor></dc:contributor>\n'
    mds += '    <dc:subject>S3M</dc:subject>\n'
    mds += '    <dc:rights>' + md[4] + '</dc:rights>\n'
    mds += '    <dc:relation>None</dc:relation>\n'
    mds += '    <dc:coverage>Global</dc:coverage>\n'
    mds += '    <dc:type>S3M Data Model</dc:type>\n'
    mds += '    <dc:identifier>' + md[0].replace('dm-', '') + '</dc:identifier>\n'
    mds += '    <dc:description>' + md[3] + '</dc:description>\n'
    mds += '    <dc:publisher>Data Insights, Inc. via Kunteksto</dc:publisher>\n'
    mds += '    <dc:date>' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '</dc:date>\n'
    mds += '    <dc:format>text/xml</dc:format>\n'
    mds += '    <dc:language>en-US</dc:language>\n'
    mds += '  </rdf:Description></rdf:RDF></xs:appinfo></xs:annotation>\n\n'
    return(mds)


def xdCount(data):
    adapterID = data[15].strip()
    mcID = data[14].strip()
    unitsID = str(uuid4())
    indent = 2
    padding = ('').rjust(indent)
    # Adapter
    xdstr = padding.rjust(indent) +  '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) +  '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'This is the Count model component used to model integers.\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#XdCountType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[10].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdCountType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="magnitude-status" type="s3m:MagnitudeStatus"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="error"  type="xs:int" default="0"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="accuracy" type="xs:int" default="0"/>\n'
    if not data[7] and not data[8] and not data[12]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value" type="xs:int"/>\n'
    if data[12]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value" type="xs:int" default="' + str(int(data[12])) + '"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value">\n'
        xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
        xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:int">\n'
        if data[7]:
            xdstr += padding.rjust(indent + 12) + '<xs:minInclusive value="' + str(int(data[7])) + '"/>\n'
        if data[8]:
            xdstr += padding.rjust(indent + 12) + '<xs:maxInclusive value="' + str(int(data[8])) + '"/>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
        xdstr += padding.rjust(indent + 8) + '</xs:element>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdcount-units" type="s3m:mc-' + unitsID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    xdstr += Units(unitsID, data)

    return(xdstr)

def xdQuantity(data):
    adapterID = data[15].strip()
    mcID = data[14].strip()
    unitsID = str(uuid4())
    indent = 2
    padding = ('').rjust(indent)
    # Adapter
    xdstr = padding.rjust(indent) +  '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) +  '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'This is the Quantity model component used to model floats.\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#XdQuantityType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[10].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdQuantityType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="magnitude-status" type="s3m:MagnitudeStatus"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="error"  type="xs:int" default="0"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="accuracy" type="xs:int" default="0"/>\n'
    if not data[7] and not data[8] and not data[12]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value" type="xs:decimal"/>\n'
    if data[12]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value" type="xs:decimal" default="' + str(data[12]) + '"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value">\n'
        xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
        xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:decimal">\n'
        if data[7]:
            xdstr += padding.rjust(indent + 12) + '<xs:minInclusive value="' + str(data[7]) + '"/>\n'
        if data[8]:
            xdstr += padding.rjust(indent + 12) + '<xs:maxInclusive value="' + str(data[8]) + '"/>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
        xdstr += padding.rjust(indent + 8) + '</xs:element>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdquantity-units" type="s3m:mc-' + unitsID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    xdstr += Units(unitsID, data)

    return(xdstr)


def xdString(data):
    adapterID = data[15].strip()
    mcID = data[14].strip()
    indent = 2
    padding = ('').rjust(indent)
    # Adapter
    xdstr = padding.rjust(indent) +  '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) +  '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'This is the String model component used to model text.\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#XdStringType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[10].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTimeStamp"/>\n'
    
    if not data[3] and not data[4] and not data[5] and not data[6] and not data[11]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string"/>\n'
        
    elif data[11] and not data[3] and not data[4] and not data[5] and not data[6]:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string" default="' + data[11].strip() + '"/>\n'
    
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value">\n'
        xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
        xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:string">\n'
        if data[5]:
            enums = data[5].split('|')
            for e in enums:
                xdstr += padding.rjust(indent + 12) + '<xs:enumeration value="' + e.strip() + '"/>\n'
        else:
            if data[3]:
                xdstr += padding.rjust(indent + 12) + '<xs:minLength value="' + data[3].strip() + '"/>\n'
            if data[4]:
                xdstr += padding.rjust(indent + 12) + '<xs:maxLength value="' + data[4].strip() + '"/>\n'
            if data[6]:
                xdstr += padding.rjust(indent + 12) + '<xs:pattern value="' + data[6].strip() + '"/>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
        xdstr += padding.rjust(indent + 8) + '</xs:element>\n'

    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdstring-language" type="xs:language" default="en-US"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


def xdTemporal(data):
    adapterID = data[15].strip()
    mcID = data[14].strip()
    indent = 2
    padding = ('').rjust(indent)
    # Adapter
    xdstr = padding.rjust(indent) +  '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) +  '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'This is the Temporal model component used to model dates, times or datetimes.\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#XdTemporalType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[10].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdTemporalType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTimeStamp"/>\n'
    if data[2].lower() == 'date':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-date" type="xs:date"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-date" type="xs:date"/>\n'

    if data[2].lower() == 'time':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-time" type="xs:time"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-time" type="xs:time"/>\n'

    if data[2].lower() == 'datetime':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-datetime" type="xs:dateTime"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-datetime" type="xs:dateTime"/>\n'

    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-datetime-stamp" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-day" type="xs:gDay"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-month" type="xs:gMonth"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-year" type="xs:gYear"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-year-month" type="xs:gYearMonth"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-month-day" type="xs:gMonthDay"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-duration" type="xs:duration"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-ymduration" type="xs:yearMonthDuration"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-dtduration" type="xs:dayTimeDuration"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


def Units(mcID, data):
    indent = 2
    padding = ('').rjust(indent)
    xdstr = padding.rjust(indent) +  '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'This is the String model component used to define Units values for Counts and Quantities.\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#XdStringType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[10].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + ' Units"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTimeStamp"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string" fixed="' + data[13].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdstring-language" type="xs:language" default="en-US"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)



def xsdData(dataID, indent, def_url, db_file):
    indent += 2
    padding = ('').rjust(indent)
    dstr = padding.rjust(indent) +  '<xs:element name="ms-' + dataID + '" substitutionGroup="s3m:Item" type="s3m:mc-' + dataID + '"/>\n'
    dstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + dataID + '">\n'
    dstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    dstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    dstr += padding.rjust(indent + 6) + 'This is the Cluster that groups all of the data items (columns) definitions into one unit.\n'
    dstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    dstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    dstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + dataID + '">\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#ClusterType"/>\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + def_url + '"/>\n'
    dstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    dstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    dstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    dstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    dstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:ClusterType">\n'
    dstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    dstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="Data Items"/>\n'

    # now we need to loop through the db and create all of the model components while keeping track so we can add them here too.
    # the dictionary uses the mc uuid as the key. The items are the complete mc code.
    mcDict = OrderedDict()
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM record")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        if row[2].lower() == 'integer':
            mcDict[row[15].strip()] = xdCount(row)
        elif row[2].lower() == 'float':
            mcDict[row[15].strip()] = xdQuantity(row)
        elif row[2].lower() in ('date', 'datetime', 'time'):
            mcDict[row[15].strip()] = xdTemporal(row)
        elif row[2].lower() == 'string':
            mcDict[row[15].strip()] = xdString(row)
        else:
            raise ValueError("Invalid datatype")

    for mc_id in mcDict.keys():
        dstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ms-' + mc_id + '"/>\n'


    dstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    dstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    dstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    dstr += padding.rjust(indent) + '</xs:complexType>\n\n'

    for mc_id in mcDict.keys():
        dstr += mcDict[mc_id]

    return(dstr)


def xsdEntry(data, db_file):
    indent = 2
    padding = ('').rjust(indent)
    dataID = str(uuid4())

    estr = padding.rjust(indent) +  '<xs:element name="ms-' + data[6].strip()  + '" substitutionGroup="s3m:Definition" type="s3m:mc-' + data[6].strip()  + '"/>\n'
    estr += padding.rjust(indent) +  '<xs:complexType name="mc-' + data[6].strip()  + '">\n'
    estr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    estr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    estr += padding.rjust(indent + 6) + 'This is the Entry container that provides all the required contextual information to manage a dataset. It is analogous to a dataset catalog entry.\n'
    estr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    estr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    estr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + data[6].strip()  + '">\n'
    estr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#EntryType"/>\n'
    estr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    estr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[4].strip() + '"/>\n'
    estr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    estr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    estr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    estr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    estr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:EntryType">\n'
    estr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    estr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[0].strip() + '"/>\n'
    estr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="entry-language" type="xs:language" fixed="en-US"/>\n'
    estr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="entry-encoding" type="xs:string" fixed="utf-8"/>\n'
    estr += padding.rjust(indent + 8) + '<!-- current-state -->\n'
    estr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" ref="s3m:ms-' + data[7].strip()  + '"/>\n'
    estr += padding.rjust(indent + 8) + '<!-- subject -->\n'
    estr += padding.rjust(indent + 8) + '<!-- provider -->\n'
    estr += padding.rjust(indent + 8) + '<!-- participations -->\n'
    estr += padding.rjust(indent + 8) + '<!-- protocol -->\n'
    estr += padding.rjust(indent + 8) + '<!-- workflow -->\n'
    estr += padding.rjust(indent + 8) + '<!-- audit -->\n'
    estr += padding.rjust(indent + 8) + '<!-- attestation -->\n'
    estr += padding.rjust(indent + 8) + '<!-- entry links -->\n'
    estr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    estr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    estr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    estr += padding.rjust(indent) + '</xs:complexType>\n\n'
    estr += xsdData(data[7].strip(), indent, data[4].strip(), db_file)
    return(estr)

def xsdDM(data):
    indent = 2
    padding = ('').rjust(indent)

    dmstr = padding.rjust(indent) +  '<xs:element name="dm-' + data[5].strip() + '" type="s3m:mc-' + data[5].strip() + '"/>\n'
    dmstr += padding.rjust(indent) +  '<xs:complexType name="mc-' + data[5].strip() + '">\n'
    dmstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    dmstr += padding.rjust(indent + 6) + data[1].strip()+'\n'
    dmstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    dmstr += padding.rjust(indent + 6) + '<rdf:Description rdf:about="mc-' + data[5].strip() + '">\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model_3_0_0.xsd#DMType"/>\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="http://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + data[4].strip() + '"/>\n'
    dmstr += padding.rjust(indent + 6) + '</rdf:Description>\n'
    dmstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    dmstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    dmstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:DMType">\n'
    dmstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    dmstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" ref="s3m:ms-' + data[6].strip() + '"/>\n'
    dmstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    dmstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    dmstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    dmstr += padding.rjust(indent) + '</xs:complexType>\n'
    return(dmstr)


def xsdRDF(xsdfile, outdir, dm_id, db_file):
    """
        Generate the RDF from the semantics embeded in the XSD.
        """

    rootdir = '.'
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dct':'http://purl.org/dc/terms/',
            'owl':'http://www.w3.org/2002/07/owl#',
            'vc':'http://www.w3.org/2007/XMLSchema-versioning',
            's3m':'http://www.s3model.com/ns/s3m/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    about = etree.XPath("//xs:annotation/xs:appinfo/rdf:Description", namespaces=nsDict)
    md = etree.XPath("//rdf:RDF/rdf:Description", namespaces=nsDict)
    rdf_file = os.open(outdir + '/dm-' + str(dm_id) + '.rdf', os.O_RDWR | os.O_CREAT)

    rdfstr = """<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' \nxmlns:s3m='http://www.s3model.com/ns/s3m/'>\n"""

    tree = etree.parse(xsdfile, parser)
    root = tree.getroot()

    rdf = about(root)
    for m in md(root):
        rdfstr += '    '+etree.tostring(m).decode('utf-8')+'\n'

    for r in rdf:
        rdfstr += '    '+etree.tostring(r).decode('utf-8')+'\n'

    # create triples for all of the elements to complexTypes
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM record")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        rdfstr += '<rdf:Description rdf:about="s3m:ms-' + row[14].strip() + '">\n'
        rdfstr += '  <s3m:isRMSOf rdf:resource="s3m:mc-' + row[14].strip() + '"/>\n'
        rdfstr += '</rdf:Description>\n'

    rdfstr += '</rdf:RDF>\n'
        
    
    os.write(rdf_file, rdfstr.encode("utf-8"))
    os.close(rdf_file)


def makeModel(db_file, outdir):
    """
    Create an S3M data model schema based on the database.
    """

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM model")
    row = c.fetchone()
    dmID = row[5].strip()

    model = outdir + '/dm-' + dmID + '.xsd'
    xsd = open(model, 'w')
    md = []
    md.append(dmID)
    md.append(row[0])
    md.append(row[3])
    md.append(row[1])
    md.append(row[2])
    def_url = row[4]
    conn.close()

    xsd_str = xsdHeader()
    xsd_str += xsdMetadata(md)
    xsd_str += xsdDM(row)
    xsd_str += xsdEntry(row, db_file)


    xsd_str += '\n</xs:schema>\n'
    # write the xsd file
    xsd.write(xsd_str)
    xsd.close()

    xsdRDF(model, outdir, dmID, db_file)
    
    return model

def xmlHdr(model, schema):
    xstr = '<s3m:dm-' + model[5].strip() + '\n'
    xstr += 'xmlns:s3m="http://www.s3model.com/ns/s3m/"\n'
    xstr += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    xstr += 'xsi:schemaLocation="http://www.s3model.com/ns/s3m/ file:' + schema + '">\n'
    xstr += '  <s3m:ms-' + model[6].strip() + '>\n'
    xstr += '    <label>' + model[0].strip() + '</label>\n'
    xstr += '    <entry-language>en-US</entry-language>\n'
    xstr += '    <entry-encoding>utf-8</entry-encoding>\n'
    xstr += '    <s3m:ms-' + model[7].strip() + '>\n'
    xstr += '      <label>Data Items</label>\n'
    return(xstr)

def xmlCount(row, data):
    xstr = '      <s3m:ms-' + row[15].strip() + '>\n'
    xstr += '      <s3m:ms-' + row[14].strip() + '>\n'
    xstr += '        <label>' + row[1].strip() + '</label>\n'
    xstr += '        <magnitude-status>equal</magnitude-status>\n'
    xstr += '        <error>0</error>\n'
    xstr += '        <accuracy>0</accuracy>\n'
    xstr += '        <xdcount-value>' + data[row[0].strip()] + '</xdcount-value>\n'
    xstr += '        <xdcount-units>\n'
    xstr += '          <label>' + row[1].strip() + ' Units</label>\n'
    xstr += '          <xdstring-value>' + row[13].strip() + '</xdstring-value>\n'
    xstr += '          <xdstring-language>en-US</xdstring-language>\n'
    xstr += '        </xdcount-units>\n'
    xstr += '      </s3m:ms-' + row[14].strip() + '>\n'
    xstr += '      </s3m:ms-' + row[15].strip() + '>\n'
    return(xstr)


def rdfCount(row, data):
    rstr = '      <rdf:Description rdf:about="s3m:ms-' + row[14].strip() + '">\n'
    rstr += '        <rdfs:label>' + row[1].strip() + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:int">' + data[row[0].strip()] + '</rdfs:value>\n'
    rstr += '      </rdf:Description>\n'
    return(rstr)


def xmlQuantity(row, data):
    xstr = '      <s3m:ms-' + row[15].strip() + '>\n'
    xstr += '      <s3m:ms-' + row[14].strip() + '>\n'
    xstr += '        <label>' + row[1].strip() + '</label>\n'
    xstr += '        <magnitude-status>equal</magnitude-status>\n'
    xstr += '        <error>0</error>\n'
    xstr += '        <accuracy>0</accuracy>\n'
    xstr += '        <xdquantity-value>' + data[row[0].strip()] + '</xdquantity-value>\n'
    xstr += '        <xdquantity-units>\n'
    xstr += '          <label>' + row[1].strip() + ' Units</label>\n'
    xstr += '          <xdstring-value>' + row[13].strip() + '</xdstring-value>\n'
    xstr += '          <xdstring-language>en-US</xdstring-language>\n'
    xstr += '        </xdquantity-units>\n'
    xstr += '      </s3m:ms-' + row[14].strip() + '>\n'
    xstr += '      </s3m:ms-' + row[15].strip() + '>\n'
    return(xstr)


def rdfQuantity(row, data):
    rstr = '      <rdf:Description rdf:about="s3m:ms-' + row[14].strip() + '">\n'
    rstr += '        <rdfs:label>' + row[1].strip() + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:decimal">' + data[row[0].strip()] + '</rdfs:value>\n'
    rstr += '      </rdf:Description>\n'
    return(rstr)


def xmlTemporal(row, data):
    xstr = '      <s3m:ms-' + row[15].strip() + '>\n'
    xstr += '      <s3m:ms-' + row[14].strip() + '>\n'
    xstr += '        <label>' + row[1].strip() + '</label>\n'
    if row[2].lower() == 'date':
        xstr += '        <xdtemporal-date>' + data[row[0].strip()] + '</xdtemporal-date>\n'
    if row[2].lower() == 'time':
        xstr += '        <xdtemporal-time>' + data[row[0].strip()] + '</xdtemporal-time>\n'
    if row[2].lower() == 'datetime':
        xstr += '        <xdtemporal-datetime>' + data[row[0].strip()] + '</xdtemporal-datetime>\n'
    xstr += '      </s3m:ms-' + row[14].strip() + '>\n'
    xstr += '      </s3m:ms-' + row[15].strip() + '>\n'
    return(xstr)


def rdfTemporal(row, data):
    rstr = '      <rdf:Description rdf:about="s3m:ms-' + row[14].strip() + '">\n'
    rstr += '        <rdfs:label>' + row[1].strip() + '</rdfs:label>\n'
    if row[2].lower() == 'date':
        rstr += '        <rdfs:value rdf:datatype="xs:date">' + data[row[0].strip()] + '</rdfs:value>\n'
    if row[2].lower() == 'time':
        rstr += '        <rdfs:value rdf:datatype="xs:time">' + data[row[0].strip()] + '</rdfs:value>\n'
    if row[2].lower() == 'datetime':
        rstr += '        <rdfs:value rdf:datatype="xs:dateTime">' + data[row[0].strip()] + '</rdfs:value>\n'
    rstr += '      </rdf:Description>\n'
    return(rstr)


def xmlString(row, data):
    xstr = '      <s3m:ms-' + row[15].strip() + '>\n'
    xstr += '      <s3m:ms-' + row[14].strip() + '>\n'
    xstr += '        <label>' + row[1].strip() + '</label>\n'
    xstr += '        <xdstring-value>' + data[row[0].strip()] + '</xdstring-value>\n'
    xstr += '        <xdstring-language>en-US</xdstring-language>\n'
    xstr += '      </s3m:ms-' + row[14].strip() + '>\n'
    xstr += '      </s3m:ms-' + row[15].strip() + '>\n'
    return(xstr)

def rdfString(row, data):
    rstr = '      <rdf:Description rdf:about="s3m:ms-' + row[14].strip() + '">\n'
    rstr += '        <rdfs:label>' + row[1].strip() + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:string">' + data[row[0].strip()] + '</rdfs:value>\n'
    rstr += '      </rdf:Description>\n'
    return(rstr)


def makeData(schema, dformat, db_file, theFile, delim, outdir):
    """
    Create data (XML or JSON) and an RDF graph based on the model.
    """
    base = os.path.basename(theFile)
    filePrefix = os.path.splitext(base)[0]
    # print('\n\nGenerate data for: ', schema, ' in ', dformat, ' using ', base)
    messagebox.showinfo('Generation', "Generate data for: " + schema + ' in ' + dformat + ' using ' + base)
    namespaces = { "http://www.s3model.com/ns/s3m/":"s3m", "http://www.w3.org/2001/XMLSchema-instance":"xsi"}
    xmldir = outdir+'/xml/'
    os.makedirs(xmldir, exist_ok=True)
    rdfdir = outdir+'/rdf/'
    os.makedirs(rdfdir, exist_ok=True)
    if dformat == 'JSON':
        jsondir = outdir+'/json/'
        os.makedirs(jsondir, exist_ok=True)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM model")
    model = c.fetchone()
    c.execute("SELECT * FROM record")
    rows = c.fetchall()
    conn.close()

    with open(theFile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delim)
        for data in reader:
            file_id = filePrefix + '-' + shortuuid.uuid()
            xmlFile = open(xmldir + file_id + '.xml', 'w')
            rdfFile = open(rdfdir + file_id + '.rdf', 'w')
            xmlStr = '<?xml version="1.0" encoding="UTF-8"?>\n'
            rdfStr = '<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\nxmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\nxmlns:s3m="http://www.s3model.com/ns/s3m/"\nxmlns:xs="http://www.w3.org/2001/XMLSchema">\n'
            rdfStr += '<rdf:Description rdf:about="' + file_id + '">\n'
            rdfStr += '  <s3m:isInstanceOf rdf:resource="dm-' + model[5].strip() + '"/>\n'
            rdfStr += '</rdf:Description>\n'

            xmlStr += xmlHdr(model, schema)

            for row in rows:
                if row[2].lower() == 'integer':
                    xmlStr += xmlCount(row, data)
                    rdfStr += rdfCount(row, data)
                elif row[2].lower() == 'float':
                    xmlStr += xmlQuantity(row, data)
                    rdfStr += rdfQuantity(row, data)
                elif row[2].lower() in ('date', 'datetime', 'time'):
                    xmlStr += xmlTemporal(row, data)
                    rdfStr += rdfTemporal(row, data)
                elif row[2].lower() == 'string':
                    xmlStr += xmlString(row, data)
                    rdfStr += rdfString(row, data)
                else:
                    raise ValueError("Invalid datatype")

            xmlStr += '    </s3m:ms-' + model[7].strip() + '>\n'
            xmlStr += '  </s3m:ms-' + model[6].strip() + '>\n'
            xmlStr += '</s3m:dm-' + model[5].strip() + '>\n'
            rdfStr += '</rdf:RDF>\n'
            xmlFile.write(xmlStr)
            xmlFile.close()
            rdfFile.write(rdfStr)
            rdfFile.close()

            if dformat == 'JSON':
                jsonFile = open(jsondir + file_id + '.json', 'w')
                with open(xmldir + file_id + '.xml', "rb") as f:    # notice the "rb" mode
                    d = xmltodict.parse(f, xml_attribs = True, process_namespaces = True, namespaces = namespaces)
                jsonStr = json.dumps(d, indent=4)
                jsonFile.write(jsonStr)
                jsonFile.close()

    return True
