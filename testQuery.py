#!/usr/bin/python
from __future__ import print_function
import psycopg2
import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def test_query():
#Testing Queries
    
    conn = None
    
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(database = cfg.get('MedData', 'database'), user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'), host = cfg.get('MedData', 'host'), port = cfg.get('MedData', 'port'))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        curr = conn.cursor()
        
        
        queryList = ConfigParser.ConfigParser()
        queryList.read('data/queryList.ini')
        
        for (each_key, each_value) in queryList.items('Query'):
            
        
            query = each_value
            print(query)
            print()
            curr.execute(query)
            rows = curr.fetchall()
        
            for r in rows:
                for c in r:
                    print(c, end=" ")
                print()
            print()
            print()
            print()
            print()
        curr.close()
        conn.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()

test_query()
