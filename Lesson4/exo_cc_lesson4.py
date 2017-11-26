# coding: utf8
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup

# open-medicaments.fr
#  - labo (index)
#  - equivalent traitement 20 (gellules) * 10 mg : dosage * nb comprimés
#  - année commerc
#  - mois commerc
#  - prix
#  - restrict age
#  - restrict poids

# pour ibuprofen

# url type no api :
#  https://open-medicaments.fr/api/v1/medicaments?limit=100&query=ibuprofene

# Faire moins de fonction quand temps limité, plus type script itératif
# On regarde la preview de la première requete pour voir si les infos viennent direct ou de l'api


def get_list(url):
    try:
        r = requests.get(url)
        return [obj['codeCIS'] for obj in json.loads(r.text)]
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return e


url_list_ibu = 'https://open-medicaments.fr/api/v1/medicaments?query=ibuprofene&api_key=ibuprofene'
dico_list = get_list(url_list_ibu)


def get_infos(code):
    url_infos = 'https://open-medicaments.fr/api/v1/medicaments/' + str(code) + '?api_key=ibuprofene'
    r = requests.get(url_infos)
    infos = json.loads(r.text)

    date_com = infos['presentations'][0]['dateDeclarationCommercialisation']
    annee = date_com.split('-')[0]
    mois = date_com.split('-')[1]

    labo = infos['titulaires'][0]

    prix = infos['presentations'][0]['prix']

    regex_poids = re.compile('(\d+) kg')
    res_poids = regex_poids.search(infos['indicationsTherapeutiques'])
    restr_poids = res_poids.group(1) if res_poids else None

    regex_age = re.compile('(\d+) ans')
    res_age = regex_age.search(infos['indicationsTherapeutiques'])
    restr_age = res_age.group(1) if res_age else None

    regex_dos = re.compile('(\d+) ([a-zA-Z]*)')
    dos = regex_dos.search(infos['compositions'][0]['substancesActives'][0]['dosageSubstance'])
    dosage = int(dos.group(1)) if dos else None
    dosage_u = dos.group(2) if dos else None
    regex_comp = re.compile('(\d+) comprim')
    res_cmp = regex_comp.search(infos['presentations'][0]['libelle'])
    nb_comp = int(res_cmp.group(1)) if res_cmp else None

    eq_trait = nb_comp * dosage if nb_comp and dosage else None
    eq_trait_u = str(eq_trait) + ' ' + dosage_u

    # print(labo, annee, mois, prix, restr_poids, restr_age, eq_trait_u)
    return [labo, annee, mois, prix, restr_poids, restr_age, eq_trait_u]


# print(list_id)
# get_infos('61000075')
# print(dico_list)
res = pd.DataFrame([get_infos(code) for code in dico_list],
                   columns=['Labo', 'Année', 'Mois', 'Prix', 'Restriction poids',
                            'Restriction Age', 'Equivalent Traitement'])
print(res)
