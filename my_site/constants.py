GET_TABLE = 'SELECT * FROM {} ORDER BY "id"'
GET_FIELD = 'SELECT * FROM {} WHERE {} = %s'
GET_COLUMN = 'SELECT {} FROM {} WHERE {} =%s'
INSERT = 'INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s)'
UPDATE = 'UPDATE {} SET {} = %s WHERE {} = %s'
DELETE = 'DELETE FROM {} WHERE {} = %s'

INSERT_USERS_TABLE = ('users', 'first_name', 'last_name', 'password', 'email')