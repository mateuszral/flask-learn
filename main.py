from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home() -> str:
    return render_template('index.html')

@app.get('/users')
def get_users() -> str:
    return '<h1>Users List</h1>'

@app.get('/users/<string:username>')
def get_user(username:str) -> str:
    return f'<h1>User: {escape(username)}</h1>'

@app.post('/users')
def create_user(user:dict) -> str:
    return f'<h1>User Created {user["name"]}</h1>'

@app.post('/login')
def login(user:dict) -> str:
    # redirect to home
    # show popup - user logged in
    return f'<h1>User logged in {user["name"]}</h1>'

@app.post('/register')
def register(user:dict) -> str:
    # redirect to home
    # show popup - user created
    return f'<h1>User registered In {user["name"]}</h1>'

@app.post('/logout')
def logout() -> str:
    # redirect to home
    # show popup - user logged out
    return f'<h1>User logout out</h1>'
