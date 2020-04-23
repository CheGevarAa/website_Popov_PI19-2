from flask import abort, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from blog import db
from blog.models import Ticket

stock = Blueprint('stock', __name__)

