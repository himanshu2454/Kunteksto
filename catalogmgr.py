"""
Load or create and load XML catalog for specific project.
"""
import os

def getCatalog(outdir, prjname):
    os.environ['XML_CATALOG_FILES'] = 'catalogs/Kunteksto_catalog.xml'

    cat_txt = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.1//EN" "http://www.oasis-open.org/committees/entity/release/1.1/catalog.dtd">
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">

  <!-- S3Model 3.0.0 RM Schema -->
  <uri name="https://www.s3model.com/ns/s3m/s3model_3_0_0.xsd" uri="../s3model/s3model_3_0_0.xsd"/>


  <!-- S3Model DMs -->
  <rewriteSystem systemIdStartString="https://dmgen.s3model.com/dmlib/" rewritePrefix="file://""" + outdir + """/ "/>
</catalog>
  
"""    
    if os.path.isfile('catalogs'+os.path.sep+prjname+'_catalog.xml'):
        os.environ['XML_CATALOG_FILES'] = 'catalogs'+os.path.sep+prjname+'_catalog.xml'
    else:
        f=open('catalogs'+os.path.sep+prjname+'_catalog.xml', 'w')
        f.write(cat_txt)
        f.close()
        os.environ['XML_CATALOG_FILES'] = 'catalogs'+os.path.sep+prjname+'_catalog.xml'
    return


        