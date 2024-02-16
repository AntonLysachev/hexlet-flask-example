from my_site.CRUD.db_util import get_connection
from psycopg2 import sql

GET_TABLE = 'SELECT * FROM {} ORDER BY "id"'
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
    except (Exception) as error:
        print(error)

    return data


def get_field(table_name, where, value):
    query = sql.SQL(GET_FIELD).format(
        sql.Identifier(table_name),
        sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchone()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)

    return data


def get_column(column_name, table_name, where, value):
    query = sql.SQL(GET_COLUMN).format(sql.Identifier(column_name),
                                       sql.Identifier(table_name),
                                       sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
    if data:
        return data[0][0]

    return data


def get_user(table_name, where, value):
    user_data = {}
    data = get_field(table_name, where, value)
    if data:
        user_data.update({'id': data[0],
                          'first_name': data[1],
                          'last_name': data[2],
                          'password': data[3],
                          'email': data[4]})

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
    except (Exception) as error:
        print(error)
        return False

    return True


def update(table_name, column_name, where, new_value, where_value):
    query = sql.SQL(UPDATE).format(sql.Identifier(table_name),
                                   sql.Identifier(column_name),
                                   sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (new_value, where_value))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
        return False

    return True


def delete(table_name, where, values):
    query = sql.SQL(DELETE).format(sql.Identifier(table_name),
                                   sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (values,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
        return False

    return True


def to_string_table(table):
    users = []
    data = get_table(table)
    for user in data:
        users.append({'id': user[0],
                      'first_name': user[1],
                      'last_name': user[2],
                      'password': user[3],
                      'email': user[4]})

    return users
