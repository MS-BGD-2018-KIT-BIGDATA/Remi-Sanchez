# coding: utf8
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup

# pandas, mean, sortbyvalue
# repo renvoie juste les 30 premiers
#


def get_token(path):
    file_token = open(path)
    return re.sub(r"\W", "", str(file_token.read()))


def get_soup(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return null


def get_most_active_users(nb):
    url = 'https://gist.github.com/paulmillr/2657075'
    soup = get_soup(url)
    list_links = soup.select("tr > td:nth-of-type(1) a")
    top_list = [a.text for a in list_links[:nb]]
    return top_list


def get_average_star_number(name):
    head = {'Authorization': 'token %s' % token}
    url = 'https://api.github.com/users/' + name + '/repos'
    res = requests.get(url, headers=head)
    repo_list = json.loads(res.text)
    if len(repo_list) == 0:
        return 0
    else:
        df = pd.DataFrame(repo_list)
        return df['stargazers_count'].mean()


def get_average_star_all(names):
    list_average = {name: get_average_star_number(name) for name in names}
    return pd.Series(list_average).sort_values(ascending=False)


token = get_token('token.txt')
top256 = get_most_active_users(256)
ranking = get_average_star_all(top256)

ranking.to_csv('ranking.csv')