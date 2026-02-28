import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.services.user_service import change_password, delete_user, edit_user, get_user_by_id
from ..utils.utils import authenticate_user


profile = Blueprint('profile', __name__)

@profile.get('/profile')
def profile_view():
    user = get_user_by_id(session['user_id'])
    if user:
        return render_template('profile.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.get('/profile/<string:user_id>')
def profile_view_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return render_template('profile.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.get('/profile/edit')
def profile_edit_view():
    user = get_user_by_id(session['user_id'])
    if user:
        return render_template('profile_edit.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.post('/profile/edit')
def profile_edit():    
    user_id = session['user_id']
    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    bio = request.form.get('bio')
    age = request.form.get('age')
    reset_avatar = request.form.get('resetAvatar')
    
    updated_user, message = edit_user(user_id, username, email, first_name, last_name, bio, age, reset_avatar)

    if not updated_user:
        flash(message, 'error')
        return redirect(url_for('profile.profile_view'))
    elif message == "No changes made to the account.":
        flash(message, 'info')
    else:
        flash(message, 'success')

    return redirect(url_for('profile.profile_view'))

@profile.post('/delete-account')
def profile_delete():
    user_id = session['user_id']
    
    deleted_user, message = delete_user(user_id)
    
    if not deleted_user:
        flash(message, 'error')
        return redirect(url_for('profile.profile_view'))
    else:
        flash(message, 'success')
        session.clear()
        return redirect(url_for('main.home'))

@profile.get('/security')
def profile_security():
    user = get_user_by_id(session['user_id'])
    if user:
        return render_template('security.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.post('/change-password')
def profile_change_password():
    user_id = session['user_id']
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_password')
    
    user, message = change_password(user_id, current_password, new_password, confirm_new_password)
    
    if not user:
        flash(message, 'error')
    else:
        flash(message, 'success')
    
    return redirect(url_for('profile.profile_security'))