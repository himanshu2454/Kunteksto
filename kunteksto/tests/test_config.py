"""
Test that the config file exists and has the manadory definitions.
"""
import configparser

class TestConf(object):

    def test_has_config(self):
        konfig = configparser.ConfigParser()
        assert konfig.read('../kunteksto.conf')

    def test_has_sqlbrow(self):
        konfig = configparser.ConfigParser()
        konfig.read('../kunteksto.conf')
        assert len(konfig['SQLITEBROWSER']['path']) > 0
        
    def test_has_status_entries(self):
        konfig = configparser.ConfigParser()
        konfig.read('../kunteksto.conf')
        assert konfig['ALLEGROGRAPH']['status'] 
        assert konfig['STARDOG']['status'] 
        assert konfig['BLAZEGRAPH']['status'] 
        assert konfig['GRAPHDB']['status'] 
        assert konfig['BASEX']['status'] 
        assert konfig['EXISTDB']['status'] 
        assert konfig['MONGODB']['status'] 
        assert konfig['COUCHDB']['status'] 
