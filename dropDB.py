#!/usr/bin/python

import psycopg2
import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def drop_db():
#Dropping Database from the server.
    
    conn = None
    
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        curr = conn.cursor()
        
        create_DB_com = "drop database " + cfg.get('MedData', 'database') + ";"
        
        curr.execute(create_DB_com)
        
        curr.close()
        conn.commit()
        print("Successful Database Drop")
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
        
