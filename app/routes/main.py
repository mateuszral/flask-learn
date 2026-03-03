from flask import Blueprint, render_template, request

from app.services.user_service import get_users_by_page, get_featured_users, search_users


main = Blueprint('main', __name__)

@main.get('/')
def home():
    featured_users = get_featured_users()
    return render_template('index.html', users=featured_users)

@main.get('/users')
def users_view():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    
    users_query = search_users(query)
    users = get_users_by_page(page, users_query)
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
