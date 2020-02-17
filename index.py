import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

# app.config['SECRET_KEY'] = 'f8f554e6ee2289a018a19ae92f1c6325'

# configuring database
#
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # MAX 20 chars
    username = db.Column(db.String(20), unique=True, nullable=False)
    # Add default image to code
    image = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.image}')"


# import secrets
# secrets.token_hex(16)
# 'f8f554e6ee2289a018a19ae92f1c6325'


# Home Page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Login Page
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

# Register Page
@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.route('/test')
def TEST():
    return "Testing..."


# Localhost setup - http://localhost:5000/
if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host='localhost', port=port)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
