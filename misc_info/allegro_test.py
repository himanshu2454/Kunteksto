from franz.openrdf.connect import ag_connect
with ag_connect('S3M_test', host='localhost', port='10035',  user='admin', password='admin') as conn:
    print(conn.size())
