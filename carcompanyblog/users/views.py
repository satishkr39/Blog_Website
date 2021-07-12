# users/views.py
from flask import render_template, flash, Blueprint, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from carcompanyblog import db
from carcompanyblog.models import User, BlogPost
from carcompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from carcompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

# total views required
# register, login, account update, logout, users list of blog posts

# Register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, username=form.username.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash("Thank You for registering")
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if  user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("you are login now")

            next = request.args.get('next')
            if next ==None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)

# Account update form
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:  # if the user uploaded picture
            username = current_user.username  # gets the current username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated')
        return redirect(url_for('users.account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename= 'profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form = form)

@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # requesting a page and this allows us to cycle through pages
    user = User.query.filter_by(username=username).first_or_404()  # grab the user and return 404 if no user exists
    # the current page numbers comes from request module.
    # pageinate is to show number of pages at bottom, and per_page is number of posts per page
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)





# logout
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Your are logged out now")
    return redirect(url_for('core.index'))
