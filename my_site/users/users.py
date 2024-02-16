from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages, session
import json
from my_site.validation.validator import validate, is_login
from my_site.CRUD.crud_utils import save, get_column, get_user, to_string_table, update, delete
from my_site.constants import INSERT_USERS_TABLE

users = Blueprint('users', __name__, template_folder='templates/users', static_folder='static')

@users.route('/', methods=['GET'])
def index():
    term = request.args.get('term')
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        users = to_string_table('users')
        if term:
            filtered_users = list(filter(lambda user: user['first_name'].lower().startswith(term.lower()), users))
            if filtered_users:
                return render_template('users.html', users=filtered_users, messages=messages, search=term)
            return render_template('users.html', users={'answer': "Совпадений не найдено"}, messages=messages, search=term)
        return render_template('users.html', users=users, messages=messages, search='')
    return redirect(url_for('auth.index'))


@users.route('/new', methods=['GET'])
def new_user():
    user = {}
    errors = {}
    return render_template('new.html', user=user, errors=errors)


@users.route('/users', methods=['POST'])
def new_user_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template('/new.html', user=user, errors=errors), 422
    save(INSERT_USERS_TABLE, user)
    user_id = str(get_column('id', 'users', 'email', user['email']))
    session.update({user_id: {'login': True}})
    response = redirect(url_for('home.index'))
    response.set_cookie('users_id', json.dumps(user_id))
    flash(f'Новый пользователь: {user["first_name"]}, добавлен', 'success')
    return response


@users.route('/<id>/settings', methods=['GET'])
def settings(id):
    messages = get_flashed_messages(with_categories=True)
    user = get_user('users', 'id', id)
    return render_template('settings.html', user=user, messages=messages)


@users.route('/<id>/edit', methods=['GET'])
def user_edit_get(id):
    errors = {}
    user = get_user('users', 'id', id)
    return render_template('edit.html', user=user, errors=errors)


@users.route('/<id>/edit', methods=['POST'])
def user_edit_post(id):
    data = request.form.to_dict()
    user = get_user('users', 'id', id)
    for column, new in data.items():
        if user[column] != new:
            update('users', column, 'id', new, id)
    flash('Данные изменены', 'success')
    return redirect(url_for('users.settings', id=id))


@users.route('/<id>/delete', methods=['POST'])
def user_delete(id):
    user = get_user('users', 'id', id)
    delete('users', 'id', id)
    response = redirect(url_for('auth.logout'))
    flash(f'Пользователь {user["first_name"]} был удален')
    return response