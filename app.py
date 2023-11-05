from flask import Flask,render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from forms import *
from BBC_scraper import teams_list
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# from Scoring import my_dict
import sqlite3
from flask_login import current_user
from flask_login import UserMixin

print(teams_list)

app = Flask(__name__)
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


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

    def get_id(self):
        return str(self.id)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process user registration
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash and salt the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in after registration
        login_user(new_user)

        flash('Your account has been created and you are now logged in!', 'success')
        return redirect(url_for('predictions'))

    return render_template('register.html')


@app.route('/')
def home():
    if current_user.is_authenticated:
        # User is already logged in, route to predictions
        return redirect(url_for('predictions'))
    else:
        # User is not logged in, route to the login page
        return redirect(url_for('login'))


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

# #run this whenever you want to delete the entries from the database
# with app.app_context():
#     db.session.query(Fixture).delete()
#     db.session.query(Prediction).delete()
#     db.session.query(Scores).delete()
#     db.session.query(User).delete()
#     db.session.commit()


with app.app_context():
    fixtures = []
    for i in range(0, len(teams_list) - 1,2):
        home_team = teams_list[i]
        away_team = teams_list[i + 1]
        existing_fixture = Fixture.query.filter_by(home_team=home_team, away_team=away_team).first()
        if existing_fixture:
            continue
        else:
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

# @app.route('/')
# def home():
#     return render_template("form.html")

# @app.route('/login', methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent = True
#         user = request.form["nm"]
#         session["user"] = user
#         #adding user to databases
#         usr=User(user)
#         db.session.add(usr)
#         db.session.commit()
#         # flash("Successfully logged in")
#         return redirect(url_for("predictions"))
#     else:
#         if "user" in session:
#             flash("Already logged in")
#             return redirect(url_for("predictions"))
#         return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # User is already logged in, route to predictions
        return redirect(url_for('predictions'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('predictions'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html')

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

# @app.route("/logout")
# def logout():
#     flash(f"you have been logged out", "info")
#     session.pop("user", None)
#     return redirect(url_for("login"))


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
            return render_template('prediction_submitted.html')
        return render_template("predictions.html", user=user, form=form, my_list=my_list)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route('/score')
def results():
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        user_id = user.id
        points = Scores.query.filter_by(user_id=user_id).first()
        print('user1')
    else:
        points = "The points have not yet been calculated."
        user = 'poo'
        print('user1')

    return render_template("score.html", user = user, score = points)



# @app.route('/score_table')
# def results_table():
#     rows = User.query.all()
#     rows_1 = Fixture.query.all()
#     return render_template("score_table_trial.html", rows=rows, rows1 = rows_1)

# @app.route('/score_table')
# def results_table():
#     # Join tables and fetch combined data
#     combined_data = db.session.query(User, Fixture, Prediction).\
#         join(Prediction, User.id == Prediction.user_id).\
#         join(Fixture, Prediction.fixture_id == Fixture.id).\
#         all()
#     for user, fixture, prediction in combined_data:
#         print("User:", user.name)
#         print("Fixture - Home Team:", fixture.home_team)
#         print("Fixture - Away Team:", fixture.away_team)
#         print("Prediction - Home Score:", prediction.home_score)
#         print("Prediction - Away Score:", prediction.away_score)
#
#     return render_template("score_table_trial.html", data = combined_data)

@app.route('/score_table', methods=['GET', 'POST'])
def results_table():
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        user_id = user.id
        points = Scores.query.filter_by(user_id=user_id).first()
        print('user1')
    else:
        points = "The points have not yet been calculated."
        user = 'poo'
        print('user1')

    users = User.query.all()

    selected_user_id = None
    if request.method == 'POST':
        selected_user_id = request.form.get('user_id')

    if selected_user_id:
        # If a user is selected, filter by the selected user ID
        all_predictions = db.session.query(User, Fixture, Prediction).\
            join(Prediction, User.id == Prediction.user_id).\
            join(Fixture, Prediction.fixture_id == Fixture.id).\
            filter(Prediction.user_id == int(selected_user_id)).all()
    else:
        # If no user is selected, fetch all predictions
        all_predictions = db.session.query(User, Fixture, Prediction).\
            join(Prediction, User.id == Prediction.user_id).\
            join(Fixture, Prediction.fixture_id == Fixture.id).all()

    return render_template("score_table_trial.html", all_predictions=all_predictions, users=users, selected_user_id=selected_user_id, user = user, score = points)


@app.route('/logout')
@login_required  # Protect the route to ensure the user is logged in
def logout():
    # Use flask-login's logout_user function to log the user out
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('/'))  # Redirect to the login page or another page after logging out


# used to drop original DB and create new one with email field
with app.app_context():
    db.drop_all()
    db.create_all()









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