from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    date = StringField('Write down the date', validators=[DataRequired()])
    submit = SubmitField('Search!')
