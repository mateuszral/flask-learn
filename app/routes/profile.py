from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user, logout_user

from app.services.user_service import change_password, delete_user, edit_user, get_user_by_id


profile = Blueprint('profile', __name__)

@profile.get('/profile')
@login_required
def profile_view():
    return render_template('profile.html', user=current_user)

@profile.get('/profile/<string:user_id>')
@login_required
def profile_view_user(user_id):
    return render_template('profile.html', user=current_user)

@profile.get('/profile/edit')
@login_required
def profile_edit_view():
    return render_template('profile_edit.html', user=current_user)

@profile.post('/profile/edit')
@login_required
def profile_edit():        
    username = request.form.get('username')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    bio = request.form.get('bio')
    age = request.form.get('age')
    avatar = request.files.get('avatar')
    reset_avatar = request.form.get('resetAvatar')
    
    updated_user, message = edit_user(current_user.id, username, email, first_name, last_name, bio, age, avatar, reset_avatar)

    if not updated_user:
        flash(message, 'error')
        return redirect(url_for('profile.profile_edit_view'))
    elif message == "No changes made to the account.":
        flash(message, 'info')
    else:
        flash(message, 'success')

    return redirect(url_for('profile.profile_edit_view'))

@profile.post('/delete-account')
@login_required
def profile_delete():    
    deleted_user, message = delete_user(current_user.id)
    
    if not deleted_user:
        flash(message, 'error')
        return redirect(url_for('profile.profile_view'))
    else:
        flash(message, 'success')
        logout_user()
        return redirect(url_for('main.home'))

@profile.get('/security')
@login_required
def profile_security():
    return render_template('security.html', user=current_user)

@profile.post('/change-password')
@login_required
def profile_change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_password')
    
    user, message = change_password(current_user.id, current_password, new_password, confirm_new_password)
    
    if not user:
        flash(message, 'error')
    else:
        flash(message, 'success')
    
    return redirect(url_for('profile.profile_security'))