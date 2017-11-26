# coding: utf8
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup

# générer un fichier de données sur le prix des Renault Zoé
# sur le marché de l'occasion en Ile de France, PACA et Aquitaine.

# source : leboncoin.fr

# fichier propre :
#   - version (3)
#   - année
#   - kilométrage
#   - prix
#   - téléphone propriétaire
#   - professionnel ou particulier
#   - colonne supp, prix de l'Argus du modèle (http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html)
#   - colonne supp, si prix > ou < à cote moyenne

# données en nombres, pas d'unités, pas de string

# https://www.leboncoin.fr/annonces/offres/ile_de_france/
# https://www.leboncoin.fr/annonces/offres/ile_de_france/?q=renault%20zoe

# q query, o page, f part/perso
# ispro
# utiliser htmllib plutot que html.parser car trop strict

# Il y a des paramètres pour la cotation spécifique sur la centrale qui utilise des cookies
# pour le modèle de la voiture
# r.cookies

# Constantes :
BASEURL = "https://www.leboncoin.fr/annonces/offres/"


def get_info_car(url):
    r = requests.get("http:" + url)
    soup = BeautifulSoup(r.text, 'html.parser')
    res = {r.text: re.sub(r"\W|[a-zA-Z]+", "", r.find_next_sibling().text) for r in soup.find_all("span", text=re.compile("Prix|Année-modèle|Kilométrage"))}
    res['Professionnel'] = 1 if soup.find("span", class_="ispro") else 0
    # Regarder si ITENS LIFE OU ZEN pour le modèle ?
    r_tel = requests.post("https://api.leboncoin.fr/api/utils/phonenumber.json", {"Refer": "https:" + url})
    # r_tel = requests.post("https://api.leboncoin.fr", {"Refer": "https:" + url})
    print(r_tel.text)
    print(res)
    return res


def get_soup(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return e


def get_list_pages(soup):
    list_links_pages = soup.find_all("a", class_="element page")
    page_links = ["http:" + a['href'] for a in list_links_pages]
    return page_links


def get_car_links_from_page(soup):
    if soup:
        list_links_items = soup.select(".list_item")
        car_links = [link['href'] for link in list_links_items if link(text=re.compile(r'Voitures'))]
        return car_links
    else:
        return []


def get_car_links_from_url(url):
    return get_car_links_from_page(get_soup(url))


def get_list_in_region(product, region):
    url = BASEURL + region + "/" + "?q=" + re.sub(r"\W", "%20", product)
    soup = get_soup(url)
    page_links = get_list_pages(soup)
    car_links = get_car_links_from_page(soup)

    for link in page_links:
        car_links.extend(get_car_links_from_url(link))

    return car_links


links = get_list_in_region("renault zoe", "ile_de_france")
print(links[0])
for link in links:
    infos = get_info_car(link)

# get_info_car(links[0])
