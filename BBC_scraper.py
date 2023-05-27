import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.co.uk/sport/football/scores-fixtures/2023-05-25"
response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')

# fixtures = soup.select("div.qa-match-block")
#
# fixtures_2 = soup.find_all('div', {'class', 'qa-match-block'})

fixtures_3 = soup.find_all("span", {'class', 'sp-c-fixture__team-name-wrap'})

# for fixture in fixtures_2:
#     home_team_1 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     away_team_1 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     home_team_2 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     away_team_2 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     home_team_3 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     away_team_3 = fixture.find("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).find_next("abbr", {'class', 'gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text.strip()
#     print(home_team_1, away_team_1, home_team_2, away_team_2, home_team_3, away_team_3)

teams_list = []
for fixture in fixtures_3:
    home_team = fixture.find("abbr", {'title','gs-u-display-block gs-u-display-none@m sp-c-fixture__team-name-trunc'}).text
    teams_list.append(home_team)

print(teams_list)