from flask import Flask, flash, redirect, render_template, request
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
    
    if email == 'admin@mybrand.com' and password == 'admin':
        flash('Login successful!', 'success')
        return redirect('/')
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@app.post('/register')
def register(user):
    # redirect to home
    # show popup - user created
    return f'<h1>User registered In {user["name"]}</h1>'

@app.post('/logout')
def logout():
    # redirect to home
    # show popup - user logged out
    return f'<h1>User logout out</h1>'

if __name__ == '__main__':
    app.run(debug=True)
