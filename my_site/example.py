from flask import Flask, request, redirect, render_template, url_for, flash, get_flashed_messages, session
import json
from my_site.validation.validator import validate, is_login, authentication
from my_site.CRUD.crud_utils import save, get_column, get_user, to_string_table , update, delete


INSERT_USERS_TABLE = ('users', 'first_name', 'last_name', 'password', 'email')

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    user = {}
    errors = {}
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        return redirect(url_for('home'))
    return render_template('index.html', user=user, errors=errors, messages=messages)


@app.post('/login')
def login():
    user = request.form.to_dict()
    errors = authentication(user)
    if errors:
        return render_template('index.html', user=user, errors=errors), 422
    user = get_user('users', 'email', user['email'])
    id = str(user['id'])
    first_name = user['first_name']
    session.update({id: {'login': True}})
    response = redirect(url_for('home'))
    response.set_cookie('users_id', json.dumps(id))
    flash(f'Вы вошли как {first_name}' , 'success')
    print(f'id: {id} | user: {first_name} | status: {session[id]}')
    return response


@app.get('/logout')
def logout():
    user_id= json.loads(request.cookies.get('users_id', json.dumps({})))
    print(user_id)
    session.update({user_id: {'login': False}})
    response = redirect(url_for('index')) 
    return response


@app.get('/home')
def home():
    user_id = json.loads(request.cookies.get('users_id', json.dumps({})))
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        return render_template('home.html', messages=messages, id=user_id)
    return redirect(url_for('index'))


@app.route('/users')
def users():
    term = request.args.get('term')
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        users = to_string_table('users')
        if term:
            filtered_users = []
            for user in users:
                if user['first_name'].lower().startswith(term.lower()):
                    filtered_users.append(user)
            if filtered_users:
                return render_template('users/index.html', users=filtered_users, messages=messages, search=term)
            return render_template('users/index.html', users={'answer': "Совпадений не найдено"}, messages=messages, search=term)
        return render_template('users/index.html', users=users, messages=messages, search='')
    return redirect(url_for('index'))


@app.get('/users/new')
def new_user():
    user = {}
    errors={}
    return render_template('users/new.html', user=user, errors=errors)


@app.post('/users')
def new_user_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template('users/new.html', user=user, errors=errors), 422
    save(INSERT_USERS_TABLE, user)
    user_id = str(get_column('id', 'users', 'email', user['email']))
    session.update({user_id: {'login': True}})
    response = redirect(url_for('home'))
    response.set_cookie('users_id', json.dumps(user_id))
    flash(f'Новый пользователь: {user["first_name"]}, добавлен', 'success')
    return response


@app.get('/user/<id>/settings')
def user_settings(id):
    messages = get_flashed_messages(with_categories=True)
    user = get_user('users', 'id', id)
    return render_template('users/settings.html', user=user, messages=messages)


@app.get('/user/<id>/edit')
def user_edit_get(id):
    errors = {}
    user = get_user('users', 'id', id)
    return render_template('users/edit.html', user=user, errors=errors)


@app.post('/user/<id>/edit')
def user_edit_post(id):
    data = request.form.to_dict()
    user = get_user('users', 'id', id)
    for column, new in data.items():
        if user[column] != new:
            update('users', column, 'id', new, id)
    flash('Данные изменены', 'success')
    return redirect(url_for('user_settings', id=id))


@app.post('/user/<id>/delete')
def user_delete(id):
    user = get_user('users', 'id', id)
    delete('users', 'id', id)
    response = redirect(url_for('logout'))
    flash(f'Пользователь {user["first_name"]} был удален')
    return response


if __name__ == '__main__':
   app.run(debug=True)