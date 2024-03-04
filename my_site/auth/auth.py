from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages, session
import json
from my_site.CRUD.crud_utils import get_user

auth = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static')

@auth.route('/')
def index():
    user = {}
    errors = {}
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        return redirect(url_for('home.index'))
    return render_template('index.html', user=user, errors=errors, messages=messages)


@auth.post('/login')
def login():
    user = request.form.to_dict()
    errors = authentication(user)
    if errors:
        return render_template('index.html', user=user, errors=errors), 422
    user = get_user('users', 'email', user['email'])
    id = str(user['id'])
    first_name = user['first_name']
    session.update({id: {'login': True}})
    response = redirect(url_for('home.index'))
    response.set_cookie('users_id', json.dumps(id))
    flash(f'Вы вошли как {first_name}', 'success')
    print(f'id: {id} | user: {first_name} | status: {session[id]}')
    return response


@auth.get('/logout')
def logout():
    user_id = json.loads(request.cookies.get('users_id', json.dumps({})))
    print(user_id)
    session.update({user_id: {'login': False}})
    response = redirect(url_for('.index'))
    return response


def authentication(user):
    errors = {}
    email = user['email']
    password = user['password']
    user = get_user('users', 'email', email)
    if not user:
        errors['email'] = 'Пользователь с таким email не зарегестрирован'
    elif password != user['password']:
        errors['password'] = 'Пароли не совпадают'
    return errors


def is_login():
    user_cookies = json.loads(request.cookies.get('users_id', json.dumps({})))
    if user_cookies:
        login = session.get(user_cookies, {})
    else:
        login = {}
    return login.get('login', False)
