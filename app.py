from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL



####################################################################
####################################################################

import pypyodbc
import pandas as pd
from datetime import datetime

def connect_to_db():
    MAX_ATTEMPTS = 3
    i = 1
    while True:
        try:
            DRIVER_NAME = 'SQL SERVER'
            SERVER_NAME = 'LAPTOP-T6NQ8T6P\SQLEXPRESS'
            DATABASE_NAME = 'aramco'
            connection_string = r'Driver={ODBC Driver 17 for SQL Server};Server=\LAPTOP-T6NQ8T6P\SQLEXPRESS;Database=aramco;Truested_Connection=Yes;TrustServerCertificate=Yes'
            conn = pypyodbc.connect(connection_string)
            return conn
        except Exception as ex:
            print(f'Error connection to database in attempt {i}: {ex}')
            if i >= MAX_ATTEMPTS:
                raise Exception('Error connecting to database',ex)
            else:
                i += 1

def get_rows(conn, sql, *param):
    cursor = conn.cursor()
    rows = cursor.execute(sql, *param).fetchall()
    cursor.close()
    return rows

def update_rows(conn, sql, *param):
    cursor = conn.cursor()
    cursor.execute(sql, *param)
    conn.commit()
    cursor.close()
def insert_row_and_get_id (conn, sql, *args):
    cursor = conn.cursor()
    cursor.execute(f'{sql}; SELECT SCOPE_IDENTITY()', *args)
    cursor.nextset()
    rows = cursor.fetchall()
    row = rows[0]
    identity = int(row[0])
    conn.commit()
    cursor.close()
    return identity

def get_my_requests (username):
    conn = connect_to_db()
    sql = "SELECT RequestId from View_Request where Requester = ?"
    rows = get_rows(conn, sql, username)
    conn.close()
    my_requests = []
    for request_row in rows:
        request_id = request_row[0]
        request
        get_request_details(request_id)
        my_requests.append(request)
    return my_requests

def insert_log(stageid, status_before, status_after, remarks, username):
    conn = connect_to_db()
    sql = "INSERT INTO Log (StageId, StatusBefore, StatusAfter, Remarks, LoginId) VALUES (?,?,?,?,?)"
    log_id= insert_row_and_get_id (conn, sql, stageid, status_before, status_after, remarks, username) conn.close()
    return log_id