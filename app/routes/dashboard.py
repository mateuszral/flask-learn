from flask import Blueprint, flash, redirect, render_template, session, url_for

from app.services.user_service import get_user_by_id


dashboard = Blueprint('dashboard', __name__)

@dashboard.get('/dashboard')
def dashboard_view():
    if 'user_id' not in session:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('auth.login_form'))
    
    user = get_user_by_id(session['user_id'])
    
    if user.change_password:
        flash('You must change your password before accessing the dashboard.', 'error')
        return redirect(url_for('profile.profile_security'))
    
    return render_template('dashboard.html', user=user)