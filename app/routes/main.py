from flask import Blueprint, render_template

from app.services.user_service import get_all_users


main = Blueprint('main', __name__)

@main.get('/')
def home():
    users = get_all_users()
    return render_template('index.html', users=users)

@main.get('/users')
def users_view():
    users = get_all_users()
    return render_template('users.html', users=users)

@main.get('/contact')
def contact_view():
    return render_template('contact.html')

@main.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
