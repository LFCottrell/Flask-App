import app
from app import *
import pandas as pd

results = pd.read_csv('mock_results.csv')

# predictions = Prediction.query.all()

with app.app_context(): # with app.app_context():
    predictions = Prediction.query.all()
    list_check = []
    second_list = []
    my_dict = {}
    for prediction in predictions:
        user_id = prediction.user_id
        list_check.append(user_id)
        if user_id not in second_list:
            my_dict[user_id] = None
            # probably not needed anymore now using dict
            second_list.append(user_id)



with app.app_context():
    all_users_points = []
    for key in my_dict:
        user_predictions = Prediction.query.filter_by(user_id=key).all()
        # this part puts all of user_id 1's predictions into a list
        fixture=[]
        for i in range(1, int(len((teams_list))/2)+1):
            pred = Prediction.query.filter_by(user_id=key, fixture_id=i).all()
            fixture.append(pred)

        # calculating the logic on those predictions, and adding the points for each game to a list
        points_list = []
        for i in range(int(len(teams_list)/2)):
            pred_1 = fixture[i][0]
            # print(pred_1)
            home_pred = pred_1.home_score
            away_pred = pred_1.away_score
            # print(home_pred,away_pred)
            home_result = results['home_team_score'][i]
            away_result = results['away_team_score'][i]

            points = 0
            # if prediction is correct
            if ((home_pred == home_result) & (away_result==away_pred)):
                points += -3
                points_list.append(points)
            # if
            if (((home_pred>away_pred) & (home_result>away_result))|((away_pred>home_pred)&(away_result>home_result))|((away_pred==home_pred)&(away_result==home_result))):
                points += -2 + abs(home_result-home_pred) + abs(away_result-away_pred)
                points_list.append(points)
            else:
                points += abs(home_result-home_pred) + abs(away_result-away_pred)
                points_list.append(points)
        total_points = sum(points_list)
        all_users_points.append(total_points)
        my_dict[key] = total_points

# adding the score to the score SQL DB

# user = User.query.get(user_id)
with app.app_context():
    for i in range(1, (len(my_dict)+1)):
        score_data = Scores(user_id=i, player_score=my_dict[i])
        print(score_data)
        db.session.add(score_data)
        db.session.commit()




print(my_dict[2])

