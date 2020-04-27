#!/usr/bin/python

import psycopg2
import ConfigParser


def create_tables():
#Create Tables in the PostgreSQL database.
    commands = (
        """
        CREATE TABLE COUNTRY(
                COUNTRY_N               VARCHAR(50) PRIMARY KEY NOT NULL,
                CONTINENT               VARCHAR(50)             NOT NULL,
                INCOME_CAT              CHAR(1),
                CHILD_MORTALITY_RATE    DECIMAL,
                MALE_LITERARY_RATE      DECIMAL,
                FEMALE_LITERARY_RATE    DECIMAL,
                MALE_LIFE_EXPECTANCY    DECIMAL,
                FEMALE_LIFE_EXPECTANCY  DECIMAL);
        """,
#There are four income categories as recognised by WHO & World Bank based on per capita GDP, they're:
#   i.  A - HIGH            (Most European countries and North America)
#   ii. B - UPPER_MIDDLE    (Some Asian like China, most Latin American Countries)
#   iii.C - LOWER_MIDDLE    (Most Asian like India, Indonesia, etc and some African countries)
#   iv. D - LOW             (African Countries)

#All the rates stored are in percentage, ie if 20 is stored that means 20%.
		"""
        CREATE TABLE PATIENT(
                ID              BIGSERIAL   PRIMARY KEY NOT NULL,
                NAME            VARCHAR(100)            NOT NULL,
                AGE             SMALLINT                NOT NULL,
                GENDER          BOOLEAN                 NOT NULL,
                COUNTRY_N       VARCHAR(50)             NOT NULL,
                INFANT          BOOLEAN                 NOT NULL,
                DISEASE         VARCHAR(50)             NOT NULL,
                FOREIGN KEY (COUNTRY_N)
                    REFERENCES COUNTRY (COUNTRY_N)
                    ON UPDATE CASCADE ON DELETE CASCADE);
        """,
# Gender is boolean cause biological you can either be male or female. True for male, false for female
# Country is a foreign key for another table
#If a person has multiple disease his entry would be multiple time
#If infant then age in months
        
        
        """
        CREATE TABLE STATUS(
                ID                  BIGSERIAL   PRIMARY KEY NOT NULL,
                ALIVE_OR_DEAD       BOOLEAN                 NOT NULL,
                RESOLVED_OR_NOT     BOOLEAN                 NOT NULL,
                YEAR_OF_DIAGNOSE    SMALLINT                NOT NULL,
                YEAR_OF_RES         SMALLINT,
                FOREIGN KEY(ID)
                    REFERENCES PATIENT (ID)
                    ON UPDATE CASCADE ON DELETE CASCADE);
        """ 
#ALIVE_OR_DEAD: True -> Alive, False -> DEAD
#RESOLVED_OR_NOT: True -> RESOLVED, False -> NOT
#If the case is still not resolved, year of resolution is NULL.
        	)

    conn = None

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('data/config.ini')
        conn = psycopg2.connect(database = cfg.get('MedData', 'database'), user = cfg.get('MedData', 'user'), password = cfg.get('MedData', 'password'), host = cfg.get('MedData', 'host'), port = cfg.get('MedData', 'port'))  #Making the Connection
        
        curr = conn.cursor()
    
        for command in commands:
            curr.execute(command)
        
        curr.close()
        
        conn.commit()
        print("Table Creation Successful")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
        
