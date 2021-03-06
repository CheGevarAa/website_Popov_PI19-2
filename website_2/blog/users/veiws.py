from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from blog import db, app, mail
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blog.users.picture_handler import add_profile_pic
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

users = Blueprint('users', __name__)

confirm = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        unique_check = User.query.filter_by(email=form.email.data).first()
        if not unique_check:
            unique_check = User.query.filter_by(username=form.username.data).first()
            if unique_check:
                return redirect(url_for('users.register'))
        else:
            return redirect(url_for('users.register'))
        token = confirm.dumps(form.email.data, salt='salt.email.confirm')
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        msg = Message('Please confirm your email!', sender='chegevara537@gmail.com', recipients=[form.email.data])
        link = url_for('users.confirmation', token=token, _external=True)
        msg.body = 'Congrats! You have been registered. Email confirmation link: {}'.format(link)
        mail.send(msg)
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/confirmation/<token>')
def confirmation(token):
    try:
        email = confirm.loads(token, salt='salt.email.confirm', max_age=900)
        return render_template('confirmation.html', email=email)
    except (SignatureExpired, BadTimeSignature):
        return render_template('token_dead.html')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return redirect(url_for('users.login'))
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Success')
            next = request.args.get('next')
            if next == None or next[0] == '/':
                next = url_for("base.index")
            return redirect(next)
    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("base.index"))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated')
        return redirect(url_for('base.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
