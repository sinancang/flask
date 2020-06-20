from flask import Flask, make_response, request, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sinancangulan'

bootstrap = Bootstrap(app)
moment = Moment(app)

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
		session['mail'] = form.mail.data
		session['pass'] = form.pass1.data
		session['gender'] = form.gender.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'))

class NameForm(FlaskForm):
	name = StringField('What is your username', validators=[DataRequired()])
	mail = StringField('What is your e-mail address', validators=[Email(), DataRequired()])
	pass1 = PasswordField('What is your password', validators=[DataRequired()])
	pass2 = PasswordField('Please verify your password', validators=[DataRequired(), EqualTo('pass1')])
	gender = SelectField('What is your gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

	submit = SubmitField('Submit')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
