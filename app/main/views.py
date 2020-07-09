from flask import current_app, flash, make_response, render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from ..meta import db
from ..models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you\'ve changed your name!')
        session['name'] = form.name.data
        user = User(username=form.name.data,
                email=form.mail.data,
                password=form.pass1.data,
                gender=form.gender.data,
                role_id = 1)
        send_email(form.mail.data, 'New User', 'mail/new_user', user=user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))

@main.route('/redirect_me')
def redirect_me():
    resp = make_response()
    resp.headers['Location']=request.args.get('location')
    return resp, '302'
