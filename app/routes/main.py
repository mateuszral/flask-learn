from flask import Blueprint, render_template

from ..utils.utils import USERS

main = Blueprint('main', __name__)

@main.get('/')
def home():
    return render_template('index.html', users=USERS)

@main.get('/users')
def users():
    return render_template('users.html')

@main.get('/contact')
def contact():
    return render_template('contact.html')

@main.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
