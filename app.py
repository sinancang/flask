from flask import Flask, make_response, request, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Message, Mail
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sinancangulan'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://root:UvD2pFnZEBkU7H@localhost/flasky"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[FLASKY]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <sinancangulan@gmail.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/redirect_me')
def redirect_me():
	resp = make_response()
	resp.headers['Location']=request.args.get('location')
	return resp, '302'

@app.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
        
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.txt', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr

class NameForm(FlaskForm):
	name = StringField('What is your username', validators=[DataRequired()])
	mail = StringField('What is your e-mail address', validators=[Email(), DataRequired()])
	pass1 = PasswordField('What is your password', validators=[DataRequired()])
	pass2 = PasswordField('Please verify your password', validators=[DataRequired(), EqualTo('pass1')])
	gender = SelectField('What is your gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

	submit = SubmitField('Submit')
    
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
