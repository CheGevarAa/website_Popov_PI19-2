from flask import abort, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from blog import db
from datetime import datetime
from blog.models import Ticket
from blog.stock.forms import SearchForm
import stripe

public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


stock = Blueprint('stock', __name__)


@stock.route('/stock_page', methods=['GET', 'POST'])
def stocks():
    form = SearchForm()
    if form.validate_on_submit():
        page_stock = request.args.get('page', 1, type=int)
        tickets = Ticket.query.filter_by(day=form.date.data + ' 00:00:00.000').paginate(page=page_stock, per_page=10)
        return render_template('stock_page.html', tickets=tickets, public_key=public_key, form=form)
    else:
        page_stock = request.args.get('page', 1, type=int)
        tickets = Ticket.query.order_by(Ticket.simple_price.desc()).paginate(page=page_stock, per_page=10)
        return render_template('stock_page.html', tickets=tickets, public_key=public_key, form=form)


@stock.route('/success')
def success():
    return render_template('success.html')


@stock.route('/charge', methods=['POST'])
def charge():

    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1000,
        currency='usd',
        description='Ticket Charge'
    )

    return redirect(url_for("stock.success"))
