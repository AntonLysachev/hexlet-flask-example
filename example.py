from flask import Flask, request, redirect, render_template, make_response, url_for, flash, get_flashed_messages, session
import json
from CRUD.validator import validate, validate_login, validate_update, is_login
from CRUD.saver import user_save, email_save_cookie
from CRUD.updator import user_update
from CRUD.deleter import user_delete
from CRUD.getter import get_user


app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    url_for('index')
    user = {}
    errors = {}
    users_cookies = json.loads(request.cookies.get('users_email', json.dumps({})))
    if users_cookies:
        login = session.get(users_cookies, {})
    else:
       login = {}
    if login.get('login', False) :
        return redirect(url_for('home'))
    return render_template('index.html', user=user, errors=errors)


@app.post('/login')
def login():
    url_for('login')
    user = request.form.to_dict()
    errors = validate_login(user)
    if errors:
        return render_template('index.html', user=user, errors=errors), 422
    user = get_user(user)
    session.update({str(user[0][0]): {'login': True}})
    response = redirect(url_for('home'))
    response.set_cookie('users_id', json.dumps(user[0][0]))
    flash(f'Вы вошли как {user[0][1]}' , 'success')
    print(f'{session[str(user[0][0])]}{user[0][1]}')
    return response

@app.post('/logout')
def logout():
    url_for('logout')
    user_id= json.loads(request.cookies.get('users_id', json.dumps({})))
    print(user_id)
    session.update({str(user_id): {'login': False}})
    return redirect('/')

@app.get('/home')
def home():
    url_for('home')
    users_cookies = json.loads(request.cookies.get('users_id', json.dumps({})))
    login = session.get(str(users_cookies), {})
    messages = get_flashed_messages(with_categories=True)
    if login.get('login', False):
        return render_template('home.html', messages=messages, session=session)
    return redirect(url_for('index'))

@app.route('/users')
def users():
    url_for('users')
    term = request.args.get('term')
    users_cookies = json.loads(request.cookies.get('users_id', json.dumps({})))
    login = session.get(str(users_cookies), {})
    messages = get_flashed_messages(with_categories=True)
    if not login.get('login', False):
        return redirect(url_for('index'))
    if term:
        filtered_users = {}
        for id, data in users.items():
            if data['first_name'].lower().startswith(term):
                filtered_users.update({id: data})
        if filtered_users:
            return render_template('users/index.html', users=filtered_users, messages=messages, search=term)
        return render_template('users/index.html', users={'answer': "Совпадений не найдено"}, messages=messages, search=term)
    return render_template('users/index.html', users=users, messages=messages, search='')


@app.get('/users/new')
def new_user():
    url_for('new_user')
    user = {}
    errors={}
    return render_template('users/new.html', user=user, errors=errors)


@app.post('/users')
def new_user_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template('users/new.html', user=user, errors=errors), 422
    user_id = user_save(user)
    session.update({str(user_id) : {'login': True}})
    response = redirect(url_for('home'))
    response.set_cookie('users_id', json.dumps(user_id))
    flash(f'Новый пользователь: {user["first_name"]}, добавлен', 'success')
    return response


@app.route('/users/<int:id>')
def user(id):
    url_for('user', id=id)
    with open('resurses/user_bd.json', 'r') as rf:
        users = json.load(rf)
        id = str(id)    
        if id in users:
          return render_template('users/show.html', user=users[id])
    return redirect('/users/page_not_found')


@app.route('/user/<id>/edit')
def edit_user(id):
    url_for('edit_user', id=id)
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
    user = db[id]
    errors = {}
    return render_template('users/edit.html', user=user, errors=errors)


@app.post('/user/<id>/patch')
def patch_user(id):
    url_for('patch_user', id=id)
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
    url_for('delete_user_get', id=id)
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
        user = db[id]
    return render_template('/users/delete.html', user=user)


@app.post('/user/<id>/delete')
def delete_user_post(id):
    url_for('delete_user_post', id=id)
    user_delete(id)
    flash("Пользователь удален", 'seccess')
    return redirect(url_for('users'))


@app.get('/users/page_not_found')
def user_page_not_found():
    url_for('user_page_not_found')
    return render_template('users/page_not_found.html')

if __name__ == '__main__':
   app.run(debug=True)