from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class FixtureForm(FlaskForm):
    home_team = StringField('Home Team')
    away_team = StringField('Away Team')
    submit = SubmitField('Submit')