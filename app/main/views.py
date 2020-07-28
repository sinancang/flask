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
