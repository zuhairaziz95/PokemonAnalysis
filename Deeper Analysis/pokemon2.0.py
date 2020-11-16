import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##from https://www.kaggle.com/mmetter/pokemon-data-analysis-tutorial?select=pokemon.csv


####--------------explanatory data analysis

pokemon = pd.read_csv("datasets_2619_4359_pokemon.csv")	
combat = pd.read_csv("datasets_2619_4359_combats.csv")
test = pd.read_csv("datasets_2619_4359_tests.csv")

#replace column name # as number column
pokemon = pokemon.rename(index=str, columns={"#": "Number"})
print(pokemon.head(10))

#acces first combat data
print(combat.head(10))

#look at the shape of data
print("Dimension of pokemon is",pokemon.shape)
print("Dimension of combat is",combat.shape)

#missing data from pokemon and combat
#1 missing data in NAME and  alot in TYPE 2 
print(pokemon.isnull().sum())

#no missing data in combat
print(combat.isnull().sum())


##investigate which missing data 
#print(pokemon[pokemon.isnull().any(axis=1)]) 
print(pokemon[pokemon['Name'].isnull()])
#print(pokemon.iloc[61])
#print(pokemon.iloc[63])


#----from pokemon pokedex we know the missign data is primeape
#fill NA with data primeape
#(pokemon['Name'][62] == "Primeape")
pokemon['Name'].fillna("Primeape",inplace=True)

##calculate the win percentage of each pokemon

total_Wins = combat.Winner.value_counts()                                     
#-get number of wins for each pokemon
numberOfWins = combat.groupby('Winner').count()
#print(numberOfWins)
countbyFirst = combat.groupby('First_pokemon').count()
countbySecond = combat.groupby('Second_pokemon').count()

print("Looking at the dimension of the dataframes")
print("Count by first win shape",countbyFirst.shape)
print("Count by second win shape",countbySecond.shape)
print("Total wins shape",total_Wins.shape)

##the dimension is different in total wins. There is one missing pokemon who 
#did no win a single fight / didnt participate

#-find losing pokemon
#offest by minus 1 cus index and number are off by one 
find_losing_p = np.setdiff1d(countbyFirst.index.values, numberOfWins.index.values)-1
losing_p = pokemon.iloc[find_losing_p[0],]
print(losing_p)


#-create a new dataframe to join new data
numberOfWins = numberOfWins.sort_index()
numberOfWins['Total Fights']= countbyFirst.Winner + countbySecond.Winner
numberOfWins['Win percentage']= numberOfWins.First_pokemon/numberOfWins['Total Fights']

#-merge the winning dataset and the original pokemon dataset
results2= pd.merge(pokemon, numberOfWins, right_index=True, left_on='Number')
results3= pd.merge(pokemon, numberOfWins, right_index=True, left_on='Number', how='left')

#-look at difference btwn two datasets to see which pokemon never has battle record

missing_p = np.setdiff1d(pokemon.index.values, results3.index.values)
#subset the dataframe where pokemon win percent is NAN
print(results3[results3['Win percentage'].isnull()])


#-Find top 10 pokemon worse win percentage
print(results3[np.isfinite(results3['Win percentage'])].sort_values(by=['Win percentage']).head(10))
#-Find top 10 pokemon best win percentage
print(results3[np.isfinite(results3['Win percentage'])].sort_values(by = ['Win percentage'], ascending = False ).head(20))


##visualize the data using graph
#-plot barplot of 1st type pokemon

sns.set_color_codes("pastel")
#ax = sns.countplot(x="Type 1", hue="Legendary", data=results3)
plt.xticks(rotation=90)
plt.xlabel('Type 1')
plt.ylabel('Total')
plt.title('Total pokemon by Type 1')
#plt.show()


#-plot barplot of 2nd type pokemon counts
sns.set_color_codes("pastel")
#ax = sns.countplot(y='Type 2', hue='Legendary', data=results3)
plt.ylabel('Type 1')
plt.xlabel('Total')
plt.title('Total pokemon by Type 2')
#plt.show()


#--group data by type and win percentage
TypeWin=results3.groupby('Type 1').agg({"Win percentage": "mean"}).sort_values(by="Win percentage", ascending=False)
print(TypeWin)



#-seaborn pairplot
'''
sns.distplot(results3["Win percentage"].dropna(), bins=20)
col = ['Type 1','HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Win Percentage']
results3.loc[:,'HP':'Speed'].corr()
sns.pairplot(results3.loc[:,col].dropna())

plt.show()


#-Pairgrid

col = ['Type 1','HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Win Percentage']

g = sns.PairGrid(results3.loc[:,col], diag_sharey=False)
g.map_lower(sns.kdeplot, cmap="Blues_d")
g.map_upper(sns.regplot)
g.map_diag(sns.kdeplot, lw=3)
'''

#-plot sns.heatmap
plt.figure(figsize=(10,6))
sns.heatmap(results3.corr(),annot=True)
plt.title('Pokemon Feature Correlation')
plt.show()