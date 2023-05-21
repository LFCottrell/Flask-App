from app import *
import pandas as pd

results = pd.read_csv('mock_results.csv')

with app.app_context():
    user_id = 1
    user_predictions = Prediction.query.filter_by(user_id=user_id).all()
    print(len(teams_list))

    # this part puts all of user_id 1's predictions into a list
    fixture=[]
    for i in range(1, int(len((teams_list))/2)+1):
        pred = Prediction.query.filter_by(user_id=user_id, fixture_id=i).all()
        fixture.append(pred)
        print(fixture)


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
        if ((home_pred == home_result) & (away_result==away_pred)):
            points += -3
            points_list.append(points)
        if (((home_pred>away_pred) & (home_result>away_result))|((away_pred>home_pred)&(away_result>home_result))|((away_pred==home_pred)&(away_result==home_result))):
            points += -2 + abs(home_result-home_pred) + abs(away_result-away_pred)
            points_list.append(points)
        else:
            points += abs(home_result-home_pred) + abs(away_result-away_pred)
            points_list.append(points)
    total_points = sum(points_list)
print(total_points)

