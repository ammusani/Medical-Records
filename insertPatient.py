#!/usr/bin/python

import psycopg2
import ConfigParser


def insert_patient():
#Insert in Patient Tables in the PostgreSQL database.
    commands = (
        """
        INSERT INTO PATIENT (NAME, AGE, GENDER, COUNTRY_N, INFANT, DISEASE) VALUES (""",
# Gender is boolean cause biological you can either be male or female. True for male, false for female
# Country is a foreign key for another table
#If a person has multiple disease his entry would be multiple time
#If infant then age in months
        """);
        """
    )

    conn = None

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(database = cfg.get('MedData', 'database'), user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'), host = cfg.get('MedData', 'host'), port = cfg.get('MedData', 'port'))  #Making the Connection
        
        patientData = ConfigParser.ConfigParser()
        patientData.read('data/patient.ini')
        curr = conn.cursor()
    
        for each_section in patientData.sections():
            query = commands[0]
            for (each_key, each_val) in patientData.items(each_section):
                if (each_key == 'id'):
                    continue
                
                if (each_key != 'disease'):
                    if(each_key == 'name' or each_key == 'country_n'):
                        query = query + "'" + each_val + "'" + ","
                    else:
                        query = query + each_val + ", "
                else:
                    query = query + "'" + each_val + "'"
            query = query + commands[1]
            curr.execute(query)
            
        curr.close()
        
        conn.commit()
        print("Patient Data Insertion Successfull")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
        
