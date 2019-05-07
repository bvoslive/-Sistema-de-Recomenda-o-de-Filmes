# K-Means Clustering

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Importing the dataset
dataset = pd.read_csv('../IMDB_2/ratings.csv', encoding='cp1252')

k=2
"""
clica= input('insira')
if(clica=='1'):
    print('deu')
"""


#CAPTURANDO
diretores = dataset.iloc[:, [1, -1]].values
data = dataset.iloc[:, -2].values
genero = dataset.iloc[:, -4].values
dir_zip=list(set(diretores[:, 1]))


Your_Rating = np.array(dataset['Your Rating'])
Year = np.array(dataset['Year'])
catch_ratings = dataset.iloc[:,[3, 1,-7, -4]].values


Rating_Year = pd.DataFrame({'Your_Rating':Your_Rating, 'Year':Year, 'Genre':genero})


horas = dataset.iloc[:, 7]

#horas = [int(x) for x in horas]

#Quantos dias passou assistindo filme
#print('Você gastou ', '%.0f' %((horas.sum()/60)/24), ' dias assistindo filme.')



#Intervalo de confiança de ano por genero

I_conf = []

generos = ['Short', 'Biography', 'War', 'History', 'Western', 'Drama', 'Crime', 'Sport', 'Sci-Fi', 'Adventure', 'Mystery', 'Thriller', 'Animation', 'Documentary', 'Action', 'Music', 'Fantasy', 'Comedy', 'Romance', 'Family', 'Musical', 'Horror']

for k in range(len(generos)):
    catch = []

    for i in range(len(Rating_Year)):
        if(generos[k] in Rating_Year['Genre'][i]):
            #print(generos[k])
            if(Rating_Year['Your_Rating']>=7).any():
                catch.append(Rating_Year['Year'][i])




    mediana = np.mean(catch)

    std = (np.std(catch))
    std = int('%.0f' %std)

    std1 = int(mediana-std)
    std2 = int(mediana+std)
    I_conf.append([generos[k], std1, std2])


I_conf = pd.DataFrame(I_conf, columns=['Gênero', 'std1', 'std2'])


















#CAPTURANDO GENEROS UNICOS
"""
generos_expandidos_lista = pd.Series(genero)
generos_expandidos = generos_expandidos_lista.str.split(', ', expand=True)

generos_notas = pd.DataFrame({'genero':generos_expandidos_lista, 'nota':Your_Rating, 'Ano':Rating_Year['Year'],
                              'Date_Rated': dataset['Date Rated']})


generos_notas['Date_Rated'] = pd.to_datetime(generos_notas['Date_Rated'], yearfirst=True)



l = []
for i in range(len(generos_expandidos.columns)):
    l = np.append(l, generos_expandidos[i].unique())

genre_uniques = pd.Series(l)
genre_uniques = genre_uniques.unique()

genre_uniques = pd.Series(genre_uniques)
genre_uniques.fillna('retirar', inplace=True)
genre_uniques = genre_uniques[genre_uniques!='retirar']
genre_uniques = genre_uniques.reset_index()
del genre_uniques['index']



genre_uniques[1]=0
matriz_genero = [[None for i in range(4)] for j in range(len(genre_uniques))]
for i in range(len(matriz_genero)):
    matriz_genero[i][0]=genre_uniques[0][i]

for p in range(len(genre_uniques)):
    cont = 0
    nota = 0
    desvio_padrao=[]

    for i in range(len(generos_expandidos_lista)):

        if(genre_uniques[0][p] in generos_expandidos_lista[i]):
            cont +=1
            nota=nota+np.copy(Your_Rating[i])
            desvio_padrao.append(Your_Rating[i])



    matriz_genero[p][1] = nota/cont
    matriz_genero[p][2] = cont
    matriz_genero[p][3] = '%.2f' %np.var(desvio_padrao, dtype='float')

matriz_genero = pd.DataFrame(matriz_genero)
matriz_genero[1] = matriz_genero[1].map(lambda x: '%.2f' %x)
matriz_genero = matriz_genero.sort_values(1, ascending=False)
matriz_genero.columns = ['Gênero', 'Nota Média', 'Contagem', 'STD_nota']


print('MATRIZ GENERO\n', matriz_genero)

#np.savez('matriz_genero.npz', matriz_genero=matriz_genero)
"""





#   ORGANIZANDO POR ANO
"""
print('ORGANIZANDO POR ANO\n')
Action = [[None for i in range(3)] for j in range(500)]
cont=0
for i in range(len(generos_notas)):
    if 'Horror' in generos_notas['genero'][i]:
        Action[cont][0] = generos_notas['nota'][i]
        Action[cont][1] = generos_notas['Ano'][i]
        Action[cont][2] = cont
        cont+=1

Action = pd.DataFrame(Action)

Action = dict(list((Action[0]).groupby(Action[1])))



for i in Action:
    print(i, Action[i].mean())
"""






#ORGANIZAR POR ANO (não deu muito certo)
"""
for i in range(1, 11):
    print(i)
    print('Média: ',np.median(Rating_Year['Year'][Rating_Year['Your_Rating']==i]))
    print('STD: ', np.std(Rating_Year['Year'][Rating_Year['Your_Rating']==i]))




ana_rating = pd.DataFrame({'Movie':catch_ratings[:,0], 'Your Rating':catch_ratings[:,1],
                           'IMDB':catch_ratings[:,2], 'Genero':catch_ratings[:,3]})
ana_rating['difference']=catch_ratings[:,1]-catch_ratings[:,2]
ana_rating = ana_rating.sort_values(by='difference', ascending=False)
ana_rating = ana_rating.reset_index()

"""



#CATEGORIZAR MELHOR DIRETOR POR NOTA
"""
def cat_dir():
    matriz_dir = [[None for j in range(4)] for i in range(len(dir_zip))]
    for i in range(len(dir_zip)):
        ator = dir_zip[i]
        cont=0
        nota=0
        for j in range(len(diretores)):
            if ator == diretores[j,1]:
                cont+=1
                nota=nota+diretores[j,0]
        if cont>0:
            nota=nota/cont

        matriz_dir[i][0]= ator
        matriz_dir[i][1]=nota
        matriz_dir[i][2] = cont
        matriz_dir[i][3]=nota*cont

    matriz_dir = sorted(matriz_dir, key=lambda x: x[1], reverse=True)



    cat_dir = pd.DataFrame(matriz_dir)


    for i in range(len(cat_dir)):

        if cat_dir[2][i] < 3:
            cat_dir = cat_dir.drop(i, axis=0)



    cat_dir2 = cat_dir




    cat_dir2 = cat_dir2.reset_index()
    del cat_dir2['index']
    cat_dir2[1] = cat_dir2[1].map(lambda x: '%.2f' %x)

    cat_dir2.columns = ['Diretor', 'Nota', 'Contagem', 'Nota*Contagem']

    return cat_dir2
print(cat_dir())
"""


