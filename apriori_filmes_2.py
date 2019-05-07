# Apriori


"""
Melhor usar esse

"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re



# Data Preprocessing
dataset2 = pd.read_csv('../Testes/ratings.csv', encoding='cp1252')
catch = dataset2.iloc[:, [-4, 1]]
catch = catch.sort_values(by='Your Rating', ascending=False)
dataset3 = catch['Genres'][catch['Your Rating']>=7]
dataset3 = pd.DataFrame(dataset3)
dataset3 = dataset3.set_index(np.arange(len(dataset3)))

ratings = pd.read_csv('../IMDB_2/ratings.csv', encoding='cp1252')

#AJUSTANDO DADOS
Base=[]
for i in range(len(dataset3)):
    teste = str(dataset3.iloc[i][0])
    dataset4 = teste.split(', ')
    Base.append(dataset4)

dataset5 = pd.DataFrame(Base)

dataset5.fillna(value=np.NaN, inplace=True)

transactions = []
for i in range(0, len(dataset5)):
    transactions.append([str(dataset5.values[i,j]) for j in range(0, len(dataset5.columns))])





# Training Apriori on the dataset
from apyori import apriori
rules = apriori(transactions, min_support = 0.003, min_confidence = 0.7, min_lift = 2, min_length = 1, max_length=3)

# Visualising the results
results = list(rules)

results = pd.DataFrame(results)

results = pd.DataFrame(results.sort_values('support', ascending=False))
results = results.reset_index(drop=True)


"""
GÊNEROS

['Short', 'Biography', 'War', 'History', 'Western', 'Drama', 'Crime', 'Sport',
  'Sci-Fi', 'Adventure', 'Mystery', 'Thriller', 'Animation', 'Documentary',
 'Action', 'Music', 'Fantasy', 'Comedy', 'Romance', 'Family', 'Musical', 'Horror']
"""


#AJUSTANDO
reforma = pd.DataFrame(results)

Base=[]
frozenset=[]

for i in range(len(reforma)):

    caracter = str(reforma['ordered_statistics'][i][0][0]).replace('frozenset({', '')
    caracter = caracter.replace('})', '')
    caracter = caracter.replace("'", "")
    Base.append([caracter])

for i in range(len(reforma)):

    caracter = str(reforma['ordered_statistics'][i][0][1]).replace('frozenset({', '')
    caracter = caracter.replace('})', '')
    caracter = caracter.replace("'", "")
    frozenset.append([caracter])

Apriori = pd.DataFrame({'Base': Base, 'Frozenset': frozenset, 'Prob': None, 'Lift': None})

for i in range(len(Apriori)):
    Apriori['Prob'][i]=reforma['ordered_statistics'][i][0][2]
    Apriori['Lift'][i]=reforma['ordered_statistics'][i][0][3]


Apriori['Score'] = Apriori['Prob']+(Apriori['Lift']/Apriori['Lift'].max())



for i in range(len(Apriori)):
    if 'nan' in Apriori['Base'][i][0] or 'nan' in Apriori['Frozenset'][i][0]:
        Apriori = Apriori.drop(i, axis=0)

Apriori = Apriori.reset_index(drop=True)

Apriori = Apriori.sort_values('Score', ascending=False)


"""
print(Apriori['Lift'].max())
print(Apriori['Lift'].min())

print(Apriori['Score'].max())
print(Apriori['Score'].min())

print(Apriori['Prob'].max())
print(Apriori['Prob'].min())
"""


#print(Apriori.sort_values('Score', ascending=False)[Apriori['Base'].isin(['Documentary'])])



#Consulta

digita = input('Gênero = ')

org_genres=[]

for i in range(len(Apriori)):
    if digita in Apriori['Base'][i][0]:
        if(Apriori['Score'][i]>1):
            org_genres.append([Apriori['Base'][i][0].split(', '), Apriori['Frozenset'][i][0], Apriori['Score'][i]])



org_genres = pd.DataFrame(org_genres)

org_genres = org_genres.sort_values(2, ascending=False)

concat = []
for i in range(len(org_genres)):
    x = org_genres[0][i]
    concat.append(np.concatenate((org_genres[1][i], x), axis=None))


concat = pd.Series(concat)

print('Generos\n', concat)


#catching
genero = ratings.iloc[:, -4].values
Your_Rating = np.array(ratings['Your Rating'])
Year = np.array(ratings['Year'])
Rating_Year = pd.DataFrame({'Your_Rating':Your_Rating, 'Year':Year, 'Genre':genero})

#mediana e std por ano
catch = []

for i in range(len(Rating_Year)):
    if(digita in Rating_Year['Genre'][i]):
        if(Rating_Year['Your_Rating']>7).any():
            catch.append(Rating_Year['Year'][i])


mediana = np.mean(catch)

std = (np.std(catch))
std = int('%.0f' %std)

std1 = int(mediana-std)
std2 = int(mediana+std)
print(std1, std2)




#PROCURANDO NO BD DO IMDB

import numpy as np
import csv
import pandas as pd
import sys
maxInt = 100000000
decrement = True

csv.field_size_limit(maxInt)





with open('../_Dataset/IMDB/title.basics.tsv', newline='', encoding='utf_8') as f:
    reader = csv.reader(f, delimiter = '\n', quotechar='\t')

    for p in range(5):

        word = concat[p]

        for row in reader:
            genre = row[0].split('\t')
            genre = genre[-1].split(',')
            ano = row[0].split('\t')
            ano = ano[5]



            if(set(word).issubset(set(genre))==True):
                try:
                    if (isinstance(int(ano), int)):
                        if (int(ano) >= std1 and int(ano) <= std2):
                            if ('tvEpisode' in row[0] or 'videoGame' in row[0] or 'tvShort' in row[0]):
                                break
                            else:
                                print(row[0])

                except:
                    break
                #print(ano)




"""
        try:
            if (int(l[0][5]) >= std1 and int(l[0][5]) <= std2):
        # with open('../Dataset/IMDB/title.basics.tsv', newline='', encoding='utf_8') as f:
        # reader = csv.reader(f, delimiter='\n', quotechar='\t')

"""