from CRUD.db_util import get_connection
from psycopg2 import sql

GET_TABLE = 'SELECT * FROM {}'
GET_FIELD = 'SELECT * FROM {} WHERE {} = %s'
GET_COLUMN = 'SELECT {} FROM {} WHERE {} =%s'
INSERT = 'INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s)'
UPDATE = 'UPDATE {} SET {} = %s WHERE {} = %s'
DELETE = 'DELETE FROM {} WHERE {} = %s'


def get_table(table_name):
    query = sql.SQL(GET_TABLE).format(sql.Identifier(table_name))
    try:
        connection = get_connection()
        cursor = connection.cursor()    
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)

    return data


def get_field(table_name, where, value):
    query = sql.SQL(GET_FIELD).format(
        sql.Identifier(table_name),
        sql.Identifier(where)
        )
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)

    return data


def get_column(column_name, table_name, where, value):
    query = sql.SQL(GET_COLUMN).format(
            sql.Identifier(column_name),
            sql.Identifier(table_name),
            sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)
    if data:
        return data[0][0]
    
    return data

def get_user(table_name, where, value):
    user_data = {}
    data = get_field(table_name, where, value)
    user_data.update({  'id': data[0][0],
                        'first_name': data[0][1],
                        'last_name': data[0][2],
                        'password': data[0][3],
                        'email': data[0][4]})
    return user_data


def save(args, user):
    first_name = user['first_name']
    last_name = user['last_name']
    password = user['password']
    email = user['email']
    list_args = map(sql.Identifier, args)
    query = sql.SQL(INSERT).format(*list_args)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (first_name, 
                                last_name, 
                                password, 
                                email,))
        connection.commit()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)
        return False

    return True


def update(table_name, column_name, where, new_value, where_value):
    query = sql.SQL(UPDATE).format(
                    sql.Identifier(table_name),
                    sql.Identifier(column_name),
                    sql.Identifier(where)
        )
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (new_value, where_value))
        connection.commit()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)
        return False

    return True


def delete(table_name, column_name, values):
    query = sql.SQL(DELETE).format(
        sql.Identifier(table_name),
        sql.Identifier(column_name)
        )
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (values,))
        connection.commit()
        cursor.close()
        connection.close()
    except(Exception) as error : 
        print(error)
        return False
    
    return True



