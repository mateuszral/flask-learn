from flask import Blueprint, render_template

from app.services.user_service import get_users_by_page, get_featured_users


main = Blueprint('main', __name__)

@main.get('/')
def home():
    featured_users = get_featured_users()
    return render_template('index.html', users=featured_users)

@main.get('/users')
@main.get('/users/<int:page>')
def users_view(page=1):
    users = get_users_by_page(page)
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
