# coding: utf8
# je veux implenter des bureaux commerciaux en france
# connaitre les distance ville à ville
# matrice en dataFrame puis csv


import googlemaps
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


# Constantes :


URL_CITIES = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
GMAP_KEY = "AIzaSyCHIKU8qnXFc8hciD6ifkz5i0uGOyWiftw"

# Fonctions :


def get_soup(url):
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return null


def get_top_cities(nb):
    soup_cities = get_soup(URL_CITIES)
    td_cities = soup_cities.select("tr > td:nth-of-type(2)")
    return [re.sub(r"\W", "", td.text) for td in td_cities[1:nb+1]]


def get_dist_matrix_response(cities):
    gmaps = googlemaps.Client(key=GMAP_KEY)
    return gmaps.distance_matrix(origins=cities, destinations=cities)


def write_dist_top_cities(path):
    cities = get_top_cities(10)
    dir_mat = get_dist_matrix_response(cities)
    df = pd.DataFrame(columns=cities, index=cities)

    for idx, row in enumerate(dir_mat["rows"]):
        for idy, elem in enumerate(row["elements"]):
            df.at[cities[idx], cities[idy]] = elem["distance"]["text"]
    print(df)
    df.to_csv(path)


write_dist_top_cities('distances.csv')
