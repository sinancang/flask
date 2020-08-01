from flask import render_template, make_response
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/redirect_me')
def redirect_me():
    resp = make_response()
    resp.headers['Location']=request.args.get('location')
    return resp, '302'

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
