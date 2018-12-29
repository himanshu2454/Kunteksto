import os

def make_catalog(config):
    """
    Create an XML Catalog based on the installation location.    
    """
    RMVERSION = config['SYSTEM']['rmversion'].replace('.', '_')
    catdir = os.path.join(os.getcwd(), 'catalogs')
    dmlib = os.path.join(os.getcwd(), 'dmlib')

    xmlcat = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xmlcat += '<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.1//EN" "http://www.oasis-open.org/committees/entity/release/1.1/catalog.dtd">'
    xmlcat += '<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">\n'
    xmlcat += '  <!-- S3Model RM Schema -->\n'
    xmlcat += '    <uri name="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd" uri="../s3model/s3model_' + RMVERSION + '.xsd"/>\n'    
    xmlcat += '  <!-- S3Model DMs -->\n'    
    xmlcat += '    <rewriteSystem systemIdStartString="https://s3model.com/dmlib/" rewritePrefix="file:///' + dmlib + '/"/>\n'    
    xmlcat += '</catalog>\n'    
    
    if not os.path.exists(dmlib):
        os.makedirs(dmlib)    
    if not os.path.exists(catdir):
        os.makedirs(catdir)
        
    with open(catdir + '/Kunteksto_catalog.xml', encoding='utf-8', 'w') as f:
        f.write(xmlcat)

    return
