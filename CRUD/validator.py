import json
import psycopg2


def validate(user):
    errors = {}
    query = 'SELECT * FROM users WHERE email = %s'
    first_name = user['first_name']
    last_name = user['last_name']
    password = user['password']
    password_conf = user['password_conf']
    email = user['email']
    try:
        conn = psycopg2.connect('postgresql://anton_lysachev:4m4QDaXXkQ6BzsGxJsgA3EV0Aal64QmW@dpg-cn6a2vmd3nmc739hflhg-a.singapore-postgres.render.com:5432/my_site_db_t590')
        cursor = conn.cursor()    
        cursor.execute(query, (email,))
        user = cursor.fetchall()
        cursor.close()
        conn.close()
        if user:
           errors['email'] = 'Пользователь с таким email уже зарегестрирован'
    except:
        print('Не удалось установить соединение с базой данных')

    if password != password_conf:
        errors['password'] = 'Паросли не совпадают'
    if len(first_name) < 3:
        errors['first_name'] = 'Короткое имя'
    if len(last_name) < 3:
        errors['last_name'] = 'Короткая фамилия'
    return errors



def validate_update(user):
  errors = {}
  first_name = user['first_name']
  last_name = user['last_name']

  if first_name:
    if len(first_name) < 3:
       errors['first_name'] = 'Короткое имя'
  if last_name:
    if len(last_name) < 3:
      errors['last_name'] = 'Короткая фамилия'
  return errors


def validate_login(user):
    errors = {}
    query = 'SELECT * FROM users WHERE email = %s'
    password = user['password']
    email = user['email']
    try:
        conn = psycopg2.connect('postgresql://anton_lysachev:4m4QDaXXkQ6BzsGxJsgA3EV0Aal64QmW@dpg-cn6a2vmd3nmc739hflhg-a.singapore-postgres.render.com:5432/my_site_db_t590')
        cursor = conn.cursor()    
        cursor.execute(query, (email,))
        user = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        print('Не удалось установить соединение с базой данных')
    if not user:
      errors['email'] = 'Пользователь с таким email не зарегестрирован'
    elif password != user[0][3]:
       errors['password'] = 'Неверный пароль'
    return errors

def is_login(session, cookie):
    for email in cookie:
        if session[email]['login']:
          return True
    return False
   