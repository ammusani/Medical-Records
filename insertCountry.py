#!/usr/bin/python

import psycopg2
import ConfigParser


def insert_country():
#Insert in Country Tables in the PostgreSQL database.
    commands = (
        """
        INSERT INTO COUNTRY (COUNTRY_N, CONTINENT, INCOME_CAT, CHILD_MORTALITY_RATE, MALE_LITERARY_RATE, FEMALE_LITERARY_RATE, MALE_LIFE_EXPECTANCY, FEMALE_LIFE_EXPECTANCY) VALUES (""",
        """);
        """
#There are four income categories as recognised by WHO & World Bank based on per capita GDP, they're:
#   i.  A - HIGH            (Most European countries and North America)
#   ii. B - UPPER_MIDDLE    (Some Asian like China, most Latin American Countries)
#   iii.C - LOWER_MIDDLE    (Most Asian like India, Indonesia, etc and some African countries)
#   iv. D - LOW             (African Countries)

#All the rates stored are in percentage, ie if 20 is stored that means 20%.
        	)

    conn = None

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(database = cfg.get('MedData', 'database'), user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'), host = cfg.get('MedData', 'host'), port = cfg.get('MedData', 'port'))  #Making the Connection
        
        countryData = ConfigParser.ConfigParser()
        countryData.read('data/country.ini')
        curr = conn.cursor()
    
        for each_section in countryData.sections():
            query = commands[0]
            for (each_key, each_val) in countryData.items(each_section):
                if (each_key != "female_life_expectancy"):
                    if(each_key == 'country_n' or each_key == 'continent' or each_key == 'income_cat'):
                        query = query + "'" + each_val + "'" + ","
                    else:
                        query = query + each_val + ", "
                else:
                    query = query + each_val
            
            query = query + commands[1]
            curr.execute(query)
            
        curr.close()
        
        conn.commit()
        print("Country Data Insertion Successfull")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
        
