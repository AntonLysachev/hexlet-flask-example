from flask import request, session
from my_site.CRUD.crud_utils import get_column, get_user
import json


def authentication(user):
    errors = {}
    email = user['email']
    password = user['password']
    user = get_user('users', 'email', email)
    if not user:
      errors['email'] = 'Пользователь с таким email не зарегестрирован'
    elif password != user['password']:
       errors['password'] = 'Неверный пароль'
    return errors


def is_login():
    users_cookies = json.loads(request.cookies.get('users_id', json.dumps({})))
    if users_cookies:
        login = session.get(users_cookies, {})
    else:
       login = {}
    return login.get('login', False)


def validate(user):
    errors = {}
    first_name = user['first_name']
    last_name = user['last_name']
    password = user['password']
    password_conf = user['password_conf']
    email = user['email']

    email = get_column('email', 'users', 'email', email)

    if email:
        errors['email'] = 'Пользователь с таким email уже зарегестрирован'
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
