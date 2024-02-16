from flask import Flask
from my_site.users.users import users
from my_site.auth.auth import auth
from my_site.home.home import home


app = Flask(__name__)
app.secret_key = "secret_key"
app.register_blueprint(auth)
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(home, url_prefix='/home')

if __name__ == '__main__':
    app.run(debug=True)
