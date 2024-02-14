import json
import psycopg2

def user_save(user):
    insert = 'INSERT INTO users(first_name, last_name, password, email) VALUES(%s, %s, %s, %s)'
    select = 'SELECT * FROM users WHERE email = %s'
    first_name = user['first_name']
    last_name = user['last_name']
    password = user['password']
    email = user['email']
    try:
        conn = psycopg2.connect('postgresql://anton_lysachev:4m4QDaXXkQ6BzsGxJsgA3EV0Aal64QmW@dpg-cn6a2vmd3nmc739hflhg-a.singapore-postgres.render.com:5432/my_site_db_t590')
        cursor = conn.cursor()
        cursor.execute(insert, (first_name, last_name, password, email,))         
        cursor.execute(select, (email,))
        user = cursor.fetchone()       
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print('Не удалось установить соединение с базой данных')
    return user[0]



def email_save_cookie(email, cookie):
    if email in cookie:
        return json.dumps(cookie)
    else:
        cookie.append(email)
        return json.dumps(cookie)