#!/usr/bin/python

import psycopg2
import ConfigParser


def insert_status():
#Insert in Status Tables in the PostgreSQL database.
    commands = (
        """
        INSERT INTO STATUS (ALIVE_OR_DEAD, RESOLVED_OR_NOT, YEAR_OF_DIAGNOSE, YEAR_OF_RES) VALUES (""",
#ALIVE_OR_DEAD: True -> Alive, False -> DEAD
#RESOLVED_OR_NOT: True -> RESOLVED, False -> NOT
#If the case is still not resolved, year of resolution is NULL.
        """);
        """
    )

    conn = None

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(database = cfg.get('MedData', 'database'), user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'), host = cfg.get('MedData', 'host'), port = cfg.get('MedData', 'port'))  #Making the Connection
        
        statusData = ConfigParser.ConfigParser()
        statusData.read('data/status.ini')
        curr = conn.cursor()
    
        for each_section in statusData.sections():
            query = commands[0]
            for (each_key, each_val) in statusData.items(each_section):
                if (each_key == 'id'):
                    continue
                
                if (each_key != 'year_of_res'):
                    query = query + each_val + ", "
                else:
                    query = query + each_val
                    
            query = query + commands[1]
            curr.execute(query)
            
        curr.close()
        
        conn.commit()
        print("Status Data Insertion Successfull")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
        
