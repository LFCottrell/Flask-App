from flask import Flask,render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from forms import *
from BBC_scraper import teams_list
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __init__(self, name):
        self.name = name

class Fixture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    player_score = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='scores')
    def __init__(self, user_id, player_score):
        self.user_id = user_id
        self.player_score = player_score


with app.app_context():
    fixtures = []
    for i in range(0, len(teams_list) - 1,2):
        home_team = teams_list[i]
        away_team = teams_list[i + 1]
        fixture = Fixture(home_team, away_team)
        fixtures.append(fixture)  # Add the fixture to the list


        # fixture = Fixture.query.filter_by(home_team=home_team, away_team=away_team).first()

    db.session.add_all(fixtures)  # Add all fixtures to the database session
    db.session.commit()



#
# class Prediction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     home_team = db.Column(db.String(50))
#     away_team = db.Column(db.String(50))
#     home_score = db.Column(db.Integer)
#     away_score = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref='predictions')

@app.route('/')
def home():
    return render_template("form.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        #adding user to databases
        usr=User(user)
        db.session.add(usr)
        db.session.commit()
        flash("Successfully logged in")
        return redirect(url_for("predictions"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("predictions"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"you have been logged out", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/predictions", methods = ['GET', 'POST'])
def predictions():
    if "user" in session:
        user = session["user"]
        form = FixtureForm()
        my_list=teams_list
        if form.validate_on_submit():
            user = User.query.filter_by(name=session["user"]).first()
            # fixtures = []
            predictions = []
            for i in range(0, len(my_list) - 1, 2):
                home_team = my_list[i]
                away_team = my_list[i + 1]
                # fixture = Fixture(home_team, away_team)
                # fixtures.append(fixture)  # Add the fixture to the list
                # print(home_team, away_team)
                # print(my_list)

                home_score = request.form['{}_score'.format(home_team)]
                away_score = request.form['{}_score'.format(away_team)]

                fixture = Fixture.query.filter_by(home_team=home_team, away_team=away_team).first()
                print(home_score, away_score)

                prediction = Prediction(user_id=user.id, fixture_id=fixture.id, home_score=home_score,
                                        away_score=away_score)
                predictions.append(prediction)

            # db.session.add_all(fixtures)
            db.session.add_all(predictions)
            db.session.commit()
            return 'prediction submitted'
        return render_template("predictions.html", user=user, form=form, my_list=my_list)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))





# @app.route('/test')
# def test():
#     return render_template("new.html")

# @app.route('/submit', methods=['POST'])
# def submit():
#     name = request.form['name']
#     email = request.form['email']
#     # Do something with the form data
#     return 'Thanks for submitting the form!'



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)