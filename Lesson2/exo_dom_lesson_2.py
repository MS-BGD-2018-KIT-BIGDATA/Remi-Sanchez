# coding: utf8
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Idées d'améliorations :
#   - gérer plusieurs ville (département et icom : code INSE des communes)
#   - trouver le numéro icom sur internet et créer tableau ville -> num
#   - automatiser liaison icom/ville
#   - lancer les années en parallèle


def get_soup(year):
    base_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
    try:
        r = requests.get(base_url + str(year))
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return null


def get_data(soup):
    trs = ['N/A', 'N/A', 'N/A', 'N/A']
    if soup:
        if soup.find("table"):
            res = soup.find_all("td", class_="libellepetit G")
            trs = [int(r.parent.select_one("td:nth-of-type(2)").text.replace(' ', '').replace('\xa0', '')) for r in res if re.search('= [ABCD]\Z', r.text)]
        else:
            print("Aucun tableau de données sur la page.")
    else:
        print("Les données n'ont pas pu être récupérées.")
    return trs


def show_money_on_period(start=2010, end=2011):
    yrange = range(start, end)
    categories = ["A", "B", "C", "D"]
    df_euros_res = pd.DataFrame(columns=categories, index=yrange)
    for y in yrange:
        df_euros_res.loc[y, categories] = get_data(get_soup(y))
    print(df_euros_res)


show_money_on_period(2009, 2016)
