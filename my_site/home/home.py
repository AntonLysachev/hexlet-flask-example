from flask import Blueprint, request, redirect, render_template, url_for, get_flashed_messages
import json
from my_site.validation.validator import is_login

home = Blueprint('home', __name__, template_folder='templates/home', static_folder='static')

@home.get('/')
def index():
    user_id = json.loads(request.cookies.get('users_id', json.dumps({})))
    messages = get_flashed_messages(with_categories=True)
    if is_login():
        return render_template('home.html', messages=messages, id=user_id)
    return redirect(url_for('auth.index'))