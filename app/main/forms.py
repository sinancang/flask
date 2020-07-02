from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class NameForm(FlaskForm):
    name = StringField('What is your username', validators=[DataRequired()])
    mail = StringField('What is your e-mail address', validators=[Email(), DataRequired()])
    pass1 = PasswordField('What is your password', validators=[DataRequired()])
    pass2 = PasswordField('Please verify your password', validators=[DataRequired(), EqualTo('pass1')])
    gender = SelectField('What is your gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    submit = SubmitField('Submit')
