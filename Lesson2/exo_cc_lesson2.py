# coding: utf8

import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_soup(url):
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return null


def get_url(marque):
    return "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-" \
          + marque + ".html#_his_"


def get_infos(marque):
    soup = get_soup(get_url(marque))
    datas = []
    ordis = soup.select('#lpBloc > li')
    for ordi in ordis[:-1]:
        prix = float(ordi.find(name="span", class_="price").text.replace('€', '.'))
        ancien_prix = prix
        if ordi.find(name="div", class_="prdtPrSt") and ordi.find(name="div", class_="prdtPrSt").text != "":
            ancien_prix = float(ordi.find(name="div", class_="prdtPrSt").text.replace(',', '.'))
        diff = ancien_prix - prix
        diff_pourcent = (diff / ancien_prix) * 100
        datas.append({"Prix actuel": prix,
                      "Prix sans remise": ancien_prix,
                      "Remise": diff,
                      "Remise (en %)": diff_pourcent})
    return pd.DataFrame(datas)


df_dell = get_infos("dell")
df_acer = get_infos("acer")
dell_rem_moy_p = (df_dell["Remise"].sum(axis=0) / df_dell["Prix sans remise"].sum(axis=0)) * 100
acer_rem_moy_p = (df_acer["Remise"].sum(axis=0) / df_acer["Prix sans remise"].sum(axis=0)) * 100
print("Remise moyenne sur les pc Dell : " + str(dell_rem_moy_p) + " %")
print("Remise moyenne sur les pc Acer : " + str(acer_rem_moy_p) + " %")
