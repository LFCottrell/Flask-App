import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.bbc.co.uk/sport/football/scores-fixtures/2023-05-25"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the score elements on the page
home_score_elements = soup.find_all(class_="sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft")
away_score_elements = soup.find_all(class_="sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft")

home_list = []
for home_result_element in home_score_elements:
    home_result = home_result_element.text.strip()
    home_list.append(home_result)
    # print(home_result)

away_list = []
for away_result_element in away_score_elements:
    away_result = away_result_element.text.strip()
    away_list.append(away_result)
    # print(away_result)

combined_zip = zip(home_list, away_list)

final_results_list = []
for i in combined_zip:
    final_results_list.append(i)

print(int(final_results_list[0][0]))