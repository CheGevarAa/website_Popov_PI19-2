from flask import render_template, request, Blueprint
from blog.models import Post

base = Blueprint('base', __name__)

@base.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)

@base.route('/info')
def info():
    return render_template('info.html')