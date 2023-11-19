from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_active(self):
        return True  # Return True for active users

    def is_authenticated(self):
        return True  # Return True for authenticated users

    def is_anonymous(self):
        return False  # Return False for anonymous users

class Fixture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Week = db.Column(db.Integer, nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fixture_id = db.Column(db.Integer, db.ForeignKey('fixture.id'), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='predictions')
    fixture = db.relationship('Fixture', backref='predictions')
    def __init__(self, user_id, fixture_id, home_score, away_score):
        self.user_id = user_id
        self.fixture_id = fixture_id
        self.home_score = home_score
        self.away_score = away_score


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # fixture_id = db.Column(db.Integer, db.ForeignKey('fixture.id'), nullable=False)
    player_score = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='scores')
    # fixture = db.relationship('Fixture', backref='scores')
    def __init__(self, user_id, player_score):
        self.user_id = user_id
        self.player_score = player_score