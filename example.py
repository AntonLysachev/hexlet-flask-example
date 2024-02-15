from flask import Flask, request, redirect, render_template, make_response, url_for, flash, get_flashed_messages, session
import json
from validation.validator import validate, validate_update, is_login, authentication
from CRUD.crud_utils import save, get_column, get_user


INSERT_USERS_TABLE = ('users', 'first_name', 'last_name', 'password', 'email')

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    user = {}
    errors = {}
    if is_login():
        return redirect(url_for('home'))
    return render_template('index.html', user=user, errors=errors)


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


@app.post('/logout')
def logout():
    user_id= json.loads(request.cookies.get('users_id', json.dumps({})))
    session.update({user_id: {'login': False}})
    user = get_user('users', 'id', user_id)
    print(f'id: {user["id"]} | user: {user["first_name"]} | status: {session[str(user["id"])]}')
    return redirect(url_for('index'))


@app.get('/home')
def home():    
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        return render_template('home.html', messages=messages)
    return redirect(url_for('index'))


@app.route('/users')
def users():
    term = request.args.get('term')
    messages = get_flashed_messages(with_categories=True)
    print('users')
    if is_login():
        if term:
            filtered_users = {}
            for id, data in users.items():
                if data['first_name'].lower().startswith(term):
                    filtered_users.update({id: data})
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


@app.route('/users/<int:id>')
def user(id):
    with open('resurses/user_bd.json', 'r') as rf:
        users = json.load(rf)
        id = str(id)    
        if id in users:
          return render_template('users/show.html', user=users[id])
    return redirect('/users/page_not_found')


@app.route('/user/<id>/edit')
def edit_user(id):
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
    user = db[id]
    errors = {}
    return render_template('users/edit.html', user=user, errors=errors)


@app.post('/user/<id>/patch')
def patch_user(id):
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
    user = db[id]
    data = request.form.to_dict()
    data['id'] = user['id']
    errors = validate_update(data)
    if errors:
        return render_template('users/edit.html', user=data, errors=errors), 422
    user.update(data)
    db[id] = user
    user_update(db)
    flash('Данные пользователя обнавлены', 'seccess')
    return redirect(url_for('users'))


@app.get('/user/<id>/delete')
def delete_user_get(id):
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
        user = db[id]
    return render_template('/users/delete.html', user=user)


@app.post('/user/<id>/delete')
def delete_user_post(id):
    user_delete(id)
    flash("Пользователь удален", 'seccess')
    return redirect(url_for('users'))


@app.get('/users/page_not_found')
def user_page_not_found():
    url_for('user_page_not_found')
    return render_template('users/page_not_found.html')

if __name__ == '__main__':
   app.run(debug=True)