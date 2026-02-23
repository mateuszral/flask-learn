import os
import uuid

from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from utils.utils import USERS, authenticate_user, admin_required


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

@app.route('/')
def home():
    return render_template('index.html', users=USERS)

@app.get('/users')
def get_users():
    return render_template('users.html')
    
@app.post('/users')
def create_user(user):
    return f'<h1>User Created {user["name"]}</h1>'

@app.get('/profile')
def profile():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        return render_template('profile.html', user=user)
    
    flash('User not found', 'error')
    return redirect(url_for('home'))

@app.post('/profile')
def update_profile():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        bio = request.form.get('bio')
        avatar = request.files.get('avatar')
        
        if user['username'] == username and user['email'] == email and user['user_info']['first_name'] == first_name and user['user_info']['last_name'] == last_name and user['user_info']['bio'] == bio and not avatar:
            flash('No changes made to the account.', 'info')
            return redirect(url_for('profile'))

        if any(u["username"] == username for u in USERS if u["id"] != session['user_id']):
            flash('Username already exists', 'error')
            return redirect(url_for('profile'))

        if any(u["email"] == email for u in USERS if u["id"] != session['user_id']):
            flash('Email already exists', 'error')
            return redirect(url_for('profile'))

        if first_name:
            user['user_info']['first_name'] = first_name
        if last_name:
            user['user_info']['last_name'] = last_name
        if bio:
            user['user_info']['bio'] = bio
            user['username'] = username
        if email:
            user['email'] = email
            
        if avatar.filename != '':
            filename = secure_filename(avatar.filename)
            upload_path = os.path.join('static/img', filename)
            avatar.save(upload_path)
            user['avatar'] = f'static/img/{filename}'
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    flash('User not found', 'error')
    return redirect(url_for('home'))

@app.post('/edit-account/<user_id>')
@admin_required
def edit_account(user_id):
    if user_id == session['user_id']:
        flash('You cannot edit your own account from the admin panel. Use the edit profile option in your profile settings.', 'error')
        return redirect(url_for('user_management'))
    
    user = next((u for u in USERS if u['id'] == user_id), None)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('user_management'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    bio = request.form.get('bio')
    reset_password = request.form.get('resetPassword')
    reset_avatar = request.form.get('resetAvatar')
    
    if user['username'] == username and user['email'] == email and user['role'] == role and user['user_info']['first_name'] == first_name and user['user_info']['last_name'] == last_name and user['user_info']['bio'] == bio:
        flash('No changes made to the account.', 'info')
        return redirect(url_for('user_management'))

    if any(u["username"] == username for u in USERS if u["id"] != user_id):
        flash('Username already exists', 'error')
        return redirect(url_for('user_management'))

    if any(u["email"] == email for u in USERS if u["id"] != user_id):
        flash('Email already exists', 'error')
        return redirect(url_for('user_management'))

    if username:
        user['username'] = username
    if email:
        user['email'] = email    
    if role in ['user', 'admin']:
        user['role'] = role
    if first_name:
        user['user_info']['first_name'] = first_name
    if last_name:
        user['user_info']['last_name'] = last_name
    if bio:
        user['user_info']['bio'] = bio
    if reset_password:
        user['password'] = generate_password_hash('defaultpassword')
        user['change_password'] = True
    if reset_avatar:
        user['avatar'] = 'static/img/default.png'

    flash('Account updated successfully!', 'success')
    return redirect(url_for('user_management'))

@app.post('/delete-account')
@app.post('/delete-account/<user_id>')
def delete_account(user_id = None):
    if user_id:
        if user_id == session['user_id']:
            flash('You cannot delete your own account from the admin panel. Use the delete account option in your profile settings.', 'error')
            return redirect(url_for('user_management'))
        
        user = next((u for u in USERS if u['id'] == user_id), None)
        if user:
            USERS.remove(user)
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found', 'error')
        
        return redirect(url_for('user_management'))
    
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        USERS.remove(user)
        session.clear()
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('home'))
    
    flash('User not found', 'error')
    return redirect(url_for('home'))

@app.get('/security')
def security():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        return render_template('security.html', user=user)
    
    flash('User not found', 'error')
    return redirect(url_for('home'))

@app.post('/change-password')
def change_password():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not authenticate_user(user['email'], current_password, USERS):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('security'))
        
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('security'))
        
        if current_password == new_password:
            flash('New password cannot be the same as the current password', 'error')
            return redirect(url_for('security'))
        
        user['password'] = generate_password_hash(new_password)
        user['change_password'] = False
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('security'))
    
    flash('User not found', 'error')
    return redirect(url_for('home'))

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/login')
def login_form():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
        
    return render_template('auth.html')

@app.post('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')
    
    authenticated_user = authenticate_user(email, password, USERS)
    if authenticated_user: 
        session['user_id'] = authenticated_user['id']

        if remember:
            session.permanent = True
        else:
            session.permanent = False

        if authenticated_user['change_password']:
            flash('Login successful! You have to change your password.', 'info')
            return redirect(url_for('security'))

        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@app.get('/forgot-password')
def forgot_password():
    if 'user_id' in session:
        return render_template('forgot_password.html')
    
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login_form'))


@app.post('/forgot-password')
def forgot_password_form():
    email = request.form.get('email')
    
    for user in USERS:
        if email == user['email']:
            flash('Password reset link sent to your email (not really, this is a demo)', 'info')
            return render_template('auth.html')
    
    flash('Email not found', 'error')
    return render_template('auth.html')

@app.get('/register')
def register_form():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
        
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
        'role': 'user',
        'change_password': False,
        'is_featured': False
    }
    
    USERS.append(new_user)
    flash('Account created successfully! You can now log in.', 'success')
    return render_template('auth.html')

@app.get('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('login_form'))
    
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    
    if user['change_password']:
        flash('You must change your password before accessing the dashboard.', 'error')
        return redirect(url_for('security'))
    
    return render_template('dashboard.html', user=user)

@app.get('/user-management')
@admin_required
def user_management():
    return render_template('user_management.html', users=USERS)

@app.get('/admin-panel')
@admin_required
def admin_panel():
    return render_template('admin_panel.html', users=USERS)

@app.post('/admin/add-user')
@admin_required
def admin_add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if any(u["email"] == email for u in USERS) or any(u["username"] == username for u in USERS):
        flash('User with username/email already exists', 'error')
        return redirect(url_for('user_management'))

    new_user = {
        'id': str(uuid.uuid4()),
        'username': username,
        'email': email,
        'password': generate_password_hash(password),
        'role': role,
        'change_password': True,
        'is_featured': False
    }

    USERS.append(new_user)
    flash('User created successfully! Have to change password on first login', 'success')
    return redirect(url_for('user_management'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
