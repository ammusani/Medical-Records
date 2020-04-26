#!/usr/bin/python

import psycopg2
import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
#Creating Database on the server.
    
    conn = None
    
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('config.ini')
        conn = psycopg2.connect(user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        curr = conn.cursor()
        
        create_DB_com = "create database " + cfg.get('MedData', 'database') + ";"
        
        curr.execute(create_DB_com)
        curr.close()
        conn.commit()
        print("Successful Database Creation")
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()

