from setuptools import setup

import configparser

config = configparser.ConfigParser()
config.read('kunteksto.conf')
VERSION = config['KUNTEKSTO']['version']

setup(
    name = 'kunteksto',
    version = VERSION,
    description = 'The Context tool for your data. This is your tool to enter the emerging data-centric, model-first approach to information management. ',
    long_description = """Kunteksto is the tool for helping data creators and data users to translate their simple CSV formatted data files into the semantically enhanced format of a S3Model data model. 
    This provides a path for existing data to be used in conjuntion with the emerging *data-centric, model first* approach in analysis, general artificial intelligence and decision support systems. 
    It also enables expanded semantics so that secondary users can better determine if the data is appropriate for their needs. 
    
    The S3Model approach opens the door for the change to a data-centric world as opposed to the current application-centric one we have now. 
    This new world will allow automatic interoperability avoiding the data quality issues created through data cleaning and massaging. 
    The importance of this capability and improved data quality is discussed in other `S3Model <https://datainsights.tech/S3Model>`_ documentation and references. 
""",
    author = 'Timothy W. Cook',
    author_email = 'tim@datainsights.tech',
    url = 'https://datainsights.tech/Kunteksto/',  
    download_url = 'https://github.com/DataInsightsInc/Kunteksto/archive/' + VERSION + '.tar.gz',  
    keywords = ['context rdf xml machine learning data-centric semantic interoperability semantics'], 
    tests_require=['pytest',],  
    setup_requires=['pytest-runner',],  
    python_requires='>=3.6',
    install_requires=[
      'agraph-python==6.1.5',
      'alabaster==0.7.10',
      'async-timeout==1.2.0',
      'Babel==2.4.0',
      'chardet==3.0.2',
      'click==6.7',
      'Cython==0.25.2',
      'docutils==0.13.1',
      'future==0.16.0',
      'imagesize==0.7.1',
      'inflection==0.3.1',
      'iso8601==0.1.11',
      'Jinja2==2.9.6',
      'lxml==3.7.3',
      'MarkupSafe==1.0',
      'multidict==2.1.4',
      'pycurl==7.43.0',
      'Pygments==2.2.0',
      'pymongo==3.4.0',
      'pytz==2017.2',
      'PyYAML==3.12',
      'requests==2.13.0',
      'shortuuid==0.5.0',
      'six==1.10.0',
      'snowballstemmer==1.2.1',
      'Sphinx==1.5.5',
      'sphinx-rtd-theme==0.2.4',
      'ujson==1.35',
      'uvloop==0.8.0',
      'xmltodict==0.10.2',
      'yarl==0.9.8',
      ],
    entry_points='''
            [console_scripts]
            kunteksto=kunteksto:kunteksto
        ''',    
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Customer Service',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Financial and Insurance Industry',
                   'Intended Audience :: Healthcare Industry',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Legal Industry',
                   'Intended Audience :: Manufacturing',
                   'Intended Audience :: Other Audience',
                   'Intended Audience :: Religion',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   ],

)