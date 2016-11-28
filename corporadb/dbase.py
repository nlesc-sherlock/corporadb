#!/usr/bin/env python

'''
description:    Common database functionality
license:        APACHE 2.0
author:         Ronald van Haren, NLeSC (r.vanharen@esciencecenter.nl)
'''

import sqlite3

def connectToDB(dbName = None):
    '''
    Connect to a specified MySQL DB and return connection and cursor objects.
    '''
    # Start DB connection
    try:
        connection = sqlite3.connect(dbName)
    except Exception as E:
        err_msg = 'Unable to connect to %s DB.'% dbName
        #logging.error((err_msg, "; %s: %s" % (E.__class__.__name__, E)))
        raise
    msg = 'Successful connected to %s DB.'%dbName
    #logging.debug(msg)
    # if the connection succeeded get a cursor
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return connection, cursor


def closeDBConnection(connection, cursor):
    '''
    Closes a connection to a DB given the connection and cursor objects
    '''
    cursor.close()
    connection.close()
    msg = 'Connection to the DB is closed.'
    #logging.debug(msg)
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
