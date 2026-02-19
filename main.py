import uuid

from flask import Flask, flash, redirect, render_template, request, session
from markupsafe import escape
from werkzeug.security import generate_password_hash

from utils.utils import authenticate_user


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
    
@app.post('/users')
def create_user(user):
    return f'<h1>User Created {user["name"]}</h1>'

@app.get('/users/<int:user_id>')
def get_user(user_id):
    for user in USERS:
        if user['id'] == str(user_id):
            return f'<h1>User: {escape(user["username"])}</h1>'
    return f'<h1>User with ID {user_id} not found</h1>'

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
    
    authenticated_user = authenticate_user(email, password, USERS)
    if authenticated_user: 
        user_id = authenticated_user['id']
        username = authenticated_user['username']
        user_email = authenticated_user['email']

        session['user_id'] = user_id
        session['username'] = username
        session['email'] = user_email

        flash('Login successful!', 'success')
        return redirect('/')
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@app.get('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.post('/forgot-password')
def forgot_password_form():
    email = request.form.get('email')
    
    for user in USERS:
        if email == user['email']:
            flash('Password reset link sent to your email (not really, this is a demo)', 'info')
            return render_template('auth.html')
    
    flash('Email not found', 'error')
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
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
