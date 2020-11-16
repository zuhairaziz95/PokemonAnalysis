import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight')

df = pd.read_csv("datasets_121_280_Pokemon.csv")
print(df.head(n=10))

#change into upper case
df.columns = df.columns.str.upper().str.replace('_','') 
print(df.head())

#show legendary pokemon
legen = df[df['LEGENDARY']==True].head(5)
print(legen)


#set name attribute at index
df = df.set_index('NAME')

##the index pokemon contain unncesecarry word like Pokemon MegaPokemon X
#remove word before Mega

df.index = df.index.str.replace(".*(?=Mega)", "")
print(df.head(10))

#drop column with # that is axis=1;axis=0 for rows so 0,1
df = df.drop(['#'],axis=1)

#show dataset columns and dataframe
print('The columns of the dataset are:',df.columns)
print('The shape of dataframe is:',df.shape)


##print type 2 pokemon
#there is few missing data
df['TYPE 2']
#some values need to be replaced or deleted
df['TYPE 2'].fillna(df['TYPE 1'], inplace = True)


#show some data and a complete row from index bulbasur

(df.loc['Bulbasaur'])#retrieve complete row index with bulbasaur
(df.iloc[0])#retrieve complete row date from index 0; integer version of loc

df.ix['Bulbasaur']#similar to loc
df.ix[0]#similar to iloc

#filtering pokemon using logical operators
dftype12= df[((df['TYPE 1']=='Fire') | (df['TYPE 1']=='Dragon')) 
			&((df['TYPE 2']=='Dragon') | (df['TYPE 2']=='Fire'))].head(3)
print(dftype12)

#print two columns of dataframe
#dftype= df[['TYPE 1', 'TYPE 2']]
#print(dftype)

#print legendary pokemon
legendGen1 = df[(df['GENERATION']==2) & (df['LEGENDARY']==True)].head(10)
legendGen= legendGen1[['TYPE 1', 'TYPE 2', 'ATTACK','LEGENDARY','GENERATION']]
print(legendGen)

#print max HP pokemon
maxHP =df['HP'].argmax()
print("Max HP pokemon :",maxHP)

#print max def pokemon
maxDef = (df['DEFENSE']).idxmax()
print("Max Def pokemon :",maxDef)

#sort pokemon by Total in ascending number 
TotalDesc = df.sort_values('TOTAL', ascending=False)#false meaning from highest tolowest val
print(TotalDesc.head(3))

#shows all the unique types in column
print('The unique pokemon types:',df['TYPE 1'].unique())
#shows number of count for unique values
print('The no of unique pokemon:',df['TYPE 1'].nunique())

#count of different type of pokemon
print(df['TYPE 1'].value_counts())
print(df['GENERATION'].value_counts())
df.groupby(['TYPE 1']).size() #same as value counts
(df['TYPE 1'] == 'Bug').sum() #count value for summation single value

#print summary of each column
df_summary = df.describe()
print(df_summary)

#print plot of graph histogram
'''
plt.hist(df['GENERATION'],bins=6, histtype="bar")
plt.xlabel('Generation')
plt.ylabel('Count')
plt.plot()
plt.show()
'''

#plot a bar graph of the number of generation 
gen_count = df['GENERATION'].value_counts()
plt.figure(figsize=(10,5))
sns.barplot(gen_count.index,gen_count.values, alpha=0.8)
plt.xlabel('Generation')
plt.ylabel('Count values')
plt.show()

#show data of strongest pokemon by types
strong = df.sort_values(by='TOTAL', ascending=False) #sorting the rows in descending 'TOTAL' order
strong.drop_duplicates(subset=['TYPE 1'], keep='first')#check TYPE 1 pokemon , keep row which strongest and drop others

print(strong[['TYPE 1','TYPE 2', 'TOTAL']])


#plot pie chart

labels = 'Water', 'Normal', 'Grass', 'Bug', 'Psychic', 'Fire', 'Electric', 'Rock', 'Other'
sizes = [112, 98, 70, 69, 57, 52, 44, 44, 175]


'''
##wrong
sizes=[
		df['Fire'].value_counts(),
		df['Water'].value_counts(),
		df['Bug'].value_counts(),
		df['Normal'].value_counts(),
		df['Poison'].value_counts(),
		df['Electric'].value_counts(),
		df['Ground'].value_counts(),
		df['Fairy'].value_counts(),
		df['Fighting'].value_counts(),
		df['Psychic'].value_counts(),
		df['Rock'].value_counts(),
		df['Ghost'].value_counts(),
		df['Ice'].value_counts(),
		df['Dragon'].value_counts(),
		df['Dark'].value_counts(),
		df['Steel'].value_counts(),
		df['Flying'].value_counts(),
		]
'''

plt.pie(sizes,labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()


#box and whisker plot
plt.subplot(2,1,1)
#plt.subplots(figsize=(15,5))
plt.title('Attack by Type 1')
sns.boxplot(x= "TYPE 1", y="ATTACK", data=df)
plt.ylim(0,200)


plt.subplot(2,1,2)
#plt.subplots(figsize=(15,5))
plt.title('Attack by Type 2')
sns.boxplot(x= "TYPE 2", y="ATTACK", data=df)
plt.ylim(0,200)
plt.show()



#plot sns.heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(),annot=True)
plt.show()


