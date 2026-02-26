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

@main.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
