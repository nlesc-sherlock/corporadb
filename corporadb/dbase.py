#!/usr/bin/env python

'''
description:    Common database functionality
license:        APACHE 2.0
author:         Ronald van Haren, NLeSC (r.vanharen@esciencecenter.nl)
'''

import psycopg2
import psycopg2.extras
from psycopg2.extensions import register_adapter, AsIs
import numpy

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def connectToDB(dbName=None, userName=None, dbPassword=None, dbHost=None,
                dbPort=None, dbCursor=psycopg2.extras.DictCursor):
    '''
    Connect to a specified PostgreSQL DB and return connection and cursor objects.
    '''
    # Start DB connection
    try:
        connectionString = "dbname='" + dbName + "'"
        if userName != None and userName != '':
            connectionString += " user='" + userName + "'"
        if dbHost != None and dbHost != '':
            connectionString += " host='" + dbHost + "'"
        if dbPassword != None and dbPassword != '':
            connectionString += " password='" + dbPassword + "'"
        if dbPort != None:
            connectionString += " port='" + str(dbPort) + "'"
        connection  = psycopg2.connect(connectionString)
        register_adapter(numpy.float64, addapt_numpy_float64)
        register_adapter(numpy.int64, addapt_numpy_int64)
    except:
        raise
    # if the connection succeeded get a cursor
    cursor = connection.cursor(cursor_factory=dbCursor)
    return connection, cursor


def closeDBConnection(connection, cursor):
    '''
    Closes a connection to a DB given the connection and cursor objects
    '''
    cursor.close()
    connection.close()
    # msg = 'Connection to the DB is closed.'
    # logging.debug(msg)
    return


def commitToDB(connection, cursor):
    '''
    Commit changes to database, rollback in case of errors
    '''
    try:
        connection.commit()
    except:
        connection.rollback()

def extract_from_db_sql(cursor, event_id, table, column):
    '''
    Extract a value from the database
    '''
    sql = "select {} from {} where id={}".format().format(table,
                                                          column, event_id)
    cursor.execute(sql)
    return cursor.fetchone()
