from flask import current_app, make_response, render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

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

def send_email(to, subject, template, **kwargs):
        msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=current_app.config['FLASKY_MAIL_SENDER'],recipients=[to])

        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.txt', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

