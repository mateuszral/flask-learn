from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.user_service import admin_edit_user, admin_create_user, delete_user, get_all_users, get_user_by_email, get_user_by_username
from app.utils.utils import admin_required

admin = Blueprint('admin', __name__)

@admin.get('/user-management')
@admin_required
def user_management():
    users = get_all_users()
    return render_template('user_management.html', users=users)

@admin.get('/admin-panel')
@admin_required
def admin_panel():
    users = get_all_users()
    return render_template('admin_panel.html', users=users)

@admin.post('/admin/add-user')
@admin_required
def admin_add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if get_user_by_username(username) or get_user_by_email(email):
        flash('User with username/email already exists', 'error')
        return redirect(url_for('admin.user_management'))

    admin_create_user(username, email, password, role)
    
    flash('User created successfully! Have to change password on first login', 'success')
    return redirect(url_for('admin.user_management'))

@admin.post('/admin/edit-user/<user_id>')
@admin_required
def admin_edit_account(user_id):
    if user_id == session['user_id']:
        flash('You cannot edit your own account from the admin panel. Use the edit profile option in your profile settings.', 'error')
        return redirect(url_for('admin.user_management'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    bio = request.form.get('bio')
    age = request.form.get('age')
    featured = request.form.get('featured') == 'on'
    reset_password = request.form.get('resetPassword')
    reset_avatar = request.form.get('resetAvatar')
    
    updated_user, message = admin_edit_user(user_id, username, email, role, first_name, last_name, bio, age, featured, reset_password, reset_avatar)

    if not updated_user:
        flash(message, 'error')
        return redirect(url_for('admin.user_management'))
    elif message == "No changes made to the account.":
        flash(message, 'info')
    else:
        flash(message, 'success')

    return redirect(url_for('admin.user_management'))

@admin.post('/admin/delete-user/<user_id>')
@admin_required
def admin_delete_account(user_id):
    if user_id == session['user_id']:
        flash('You cannot delete your own account from the admin panel. Use the delete account option in your profile settings.', 'error')
        return redirect(url_for('admin.user_management'))
        
    user, message = delete_user(user_id)
    
    if not user:
        flash(message, 'error')
    else:
        flash(message, 'success')
        
    return redirect(url_for('admin.user_management'))