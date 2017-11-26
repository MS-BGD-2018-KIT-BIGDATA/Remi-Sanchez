# coding: utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def clean(x):
    return str(x).split('- ')[1]


df = pd.read_csv('med_gen.csv', sep=';',
                 usecols=['DEPARTEMENT', 'TOTAL DES HONORAIRES (Euros)', 'DEPASSEMENTS (Euros)'],
                 converters={'DEPARTEMENT': clean}
                 )

df['DEP/TOT'] = df['DEPASSEMENTS (Euros)'] / df['TOTAL DES HONORAIRES (Euros)']

print(df.dtypes)
print(df)

maxi = df['DEP/TOT'].max()
print(maxi)

fig = plt.figure(figsize=(20, 10))
# Custom adjust of the subplots
# plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)
#Let's create a basemap of Europe
x1 = -5.0
x2 = 12.
y1 = 40.
y2 = 54.

m = Basemap(resolution='i', projection='merc', llcrnrlat=y1, urcrnrlat=y2, llcrnrlon=x1, urcrnrlon=x2,
            lat_ts=(x1 + x2) / 2)
m.drawcountries(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(y1, y2, 2.), labels=[1, 0, 0, 0], color='black', dashes=[1, 0], labelstyle='+/-',
                linewidth=0.2)  # draw parallels
m.drawmeridians(np.arange(x1, x2, 2.), labels=[0, 0, 0, 1], color='black', dashes=[1, 0], labelstyle='+/-',
                linewidth=0.2)  # draw meridians

from matplotlib.collections import LineCollection
from matplotlib import cm
from matplotlib import colors
import shapefile

r = shapefile.Reader(r"borders/FRA_adm3")
shapes = r.shapes()
records = r.records()

# Gestion de la couleur
pu = plt.get_cmap('Reds')
# mettre vmin à 0 ou bien à la min de la densité ?
cNorm = colors.Normalize(vmin=0, vmax=maxi)
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=pu)

for record, shape in zip(records, shapes):
    lons, lats = zip(*shape.points)
    data = np.array(m(lons, lats)).T

    if len(shape.parts) == 1:
        segs = [data, ]
    else:
        segs = []
        for i in range(1, len(shape.parts)):
            index = shape.parts[i - 1]
            index2 = shape.parts[i]
            segs.append(data[index:index2])
        segs.append(data[index2:])

    lines = LineCollection(segs, antialiaseds=(1,))
    # print(record)
    # faire plus beau
    if record[6] == "Alpes-de-Haute-Provence":
        name = "Alpes-Hte-Provence"
    elif record[6] == "Territoire de Belfort":
        name = "Terr. de Belfort"
    elif record[6] == "Seine-Saint-Denis":
        name = "Seine-St-Denis"
    elif record[6] == "Paris":
        name = "Paris (Ville)"
    else:
        name = record[6]
    print("rec : ", name)
    # erreurs pour (dans rec):
    #   - Alpes-de-Haute-Provence -> Alpes-Hte-Provence
    #   - Territoire de Belfort -> Terr. de Belfort
    #   - Seine-Saint-Denis -> Seine-St-Denis
    #   - Paris -> Paris (Ville)


    dep = df.loc[df['DEPARTEMENT'] == name]
    print(dep['DEP/TOT'])
    dens = 0
    colorVal = scalarMap.to_rgba(dep['DEP/TOT'])
    lines.set_facecolors(colorVal)
    lines.set_edgecolors('k')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)

plt.savefig('france2.png', dpi=300)
plt.show()