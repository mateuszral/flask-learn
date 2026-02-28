from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from app.services.user_service import get_user_by_id


dashboard = Blueprint('dashboard', __name__)

@dashboard.get('/dashboard')
@login_required
def dashboard_view():
    user = get_user_by_id(current_user.id)
    
    if user.change_password:
        flash('You must change your password before accessing the dashboard.', 'error')
        return redirect(url_for('profile.profile_security'))
    
    return render_template('dashboard.html', user=user)