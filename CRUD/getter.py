import psycopg2

def get_user(user):
    query = 'SELECT * FROM users WHERE email = %s'
    email = user['email']
    try:
        conn = psycopg2.connect('postgresql://anton_lysachev:4m4QDaXXkQ6BzsGxJsgA3EV0Aal64QmW@dpg-cn6a2vmd3nmc739hflhg-a.singapore-postgres.render.com:5432/my_site_db_t590')
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        user = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print('Не удалось установить соединение с базой данных')
    return user