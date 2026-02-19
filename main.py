import uuid

from flask import Flask, flash, redirect, render_template, request, session
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

USERS = [
    {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@admin.com",
        "password": generate_password_hash("admin")
    },
    {
        "id": str(uuid.uuid4()),
        "username": "johndoe",
        "email": "john@example.com",
        "password": generate_password_hash("password123")
    },
    {
        "id": str(uuid.uuid4()),
        "username": "janedoe",
        "email": "jane@example.com",
        "password": generate_password_hash("securepass")
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.get('/users')
def get_users():
    return render_template('users.html')

@app.get('/users/<string:username>')
def get_user(username):
    return f'<h1>User: {escape(username)}</h1>'

@app.post('/users')
def create_user(user):
    return f'<h1>User Created {user["name"]}</h1>'

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/login')
def login_form():
    return render_template('auth.html')

@app.post('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    # todo later
    # is_remember = request.form.get('remember')
    
    for user in USERS:
        if email == user['email'] and check_password_hash(user['password'], password): 
            user_id = user['id']
            username = user['username']
            user_email = user['email']

            session['user_id'] = user_id
            session['username'] = username
            session['email'] = user_email

            flash('Login successful!', 'success')
            return redirect('/')
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@app.post('/register')
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    for user in USERS:
        if username == user['username'] or email == user['email']:
            flash('User with username/email already exists', 'error')
            return render_template('auth.html')
        
    if password != confirm_password:
        flash('Passwords are not the same', 'error')
        return render_template('auth.html')
        
    new_user = {
        'id': str(uuid.uuid4()),
        'username': username,
        'email': email,
        'password': generate_password_hash(password),
    }
    
    USERS.append(new_user)
    flash('Account created successfully! You can now log in.', 'success')
    return render_template('auth.html')

@app.get('/logout')
def logout():
    # redirect to home
    # show popup - user logged out
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
