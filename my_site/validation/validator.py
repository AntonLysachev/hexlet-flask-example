from flask import request, session
from my_site.CRUD.crud_utils import get_column, get_user


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

    if len(first_name) < 3:
        errors['first_name'] = 'Короткое имя'
    if len(last_name) < 3:
        errors['last_name'] = 'Короткая фамилия'
    return errors
