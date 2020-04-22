from flask import abort, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.blog_posts.forms import PostForm

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        blog_post = Post(title=form.title.data,
                         text=form.text.data,
                         user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Done')
        return redirect(url_for('base.index'))
    return render_template('create_post.html', form=form)


@blog_posts.route('/<int:blog_post_id>')
def read_post(blog_post_id):
    blog_post = Post.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                           date=blog_post.date, post=blog_post)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = Post.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Done Up')
        return redirect(url_for('blog_posts.read_post', blog_post_id=blog_post_id,))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Updating', form=form)


@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(blog_post_id):
    blog_post = Post.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Deleted')
    return redirect(url_for('base.index'))
