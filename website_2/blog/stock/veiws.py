from flask import abort, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from blog import db
from blog.models import Ticket

stock = Blueprint('stock', __name__)


@stock.route('/stock_page')
def stocks():
    page_stock = request.args.get('page', 1, type=int)
    tickets = Ticket.query.order_by(Ticket.date.desc()).paginate(page=page_stock, per_page=10)
    return render_template('stock_pages.html', tickets=tickets)
