from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403
