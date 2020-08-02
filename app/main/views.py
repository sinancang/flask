from flask import render_template, make_response, redirect, url_for, flash
from . import main
from ..models import User
from flask_login import login_required, current_user
from .forms import EditProfileForm
from ..meta import db

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

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
