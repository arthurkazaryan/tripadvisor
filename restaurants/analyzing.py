import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

dataframes = []
for elem in Path.cwd().joinpath('restaurants', 'pages').iterdir():
    dataframes.append(pd.read_excel(elem))
dataframe = pd.concat(dataframes)
dataframe.drop_duplicates(subset=["Name"], inplace=True)
dataframe.reset_index(inplace=True)
dataframe['Price range'] = dataframe['Price range'].str.replace('RUB', '')
dataframe[['Price from', 'Price to']] = dataframe['Price range'].str.split(' - ', 1, expand=True)
dataframe.drop(['Unnamed: 0', 'index', 'Price range'], axis=1, inplace=True)

# Plot prices data
fig, axs = plt.subplots(ncols=2, figsize=(16, 5))
ranges = [0, 500, 1000, 2000, 5000]
prices_dataframe = dataframe.copy()
for idx, col_name in enumerate(['Price from', 'Price to']):
    prices_dataframe = prices_dataframe[prices_dataframe[col_name] != 'no_data']
    prices_dataframe = prices_dataframe[prices_dataframe[col_name] != None]
    prices_dataframe[col_name] = prices_dataframe[col_name].str.replace(',', '')
    prices_dataframe[col_name] = prices_dataframe[col_name].astype(int)
    sns.barplot(x=col_name, y="Count",
                data=pd.DataFrame(prices_dataframe.groupby(
                    pd.cut(prices_dataframe[col_name], ranges)).count()[col_name]).rename(
                    columns={col_name: "Count"}).reset_index(),
                palette="Blues_d", ax=axs[idx])
fig.savefig(Path.cwd().joinpath('restaurants', 'prices_from_to.png'))

# Plot diet info
special_diets = {}
for row in dataframe['Special diets']:
    for diet in row.split(', '):
        if diet != 'no_data':
            if diet not in special_diets:
                special_diets[diet] = 0
            special_diets[diet] += 1
new_special_diets = {'Diet': [], 'Count': []}
for diet, count in special_diets.items():
    new_special_diets['Diet'].append(diet)
    new_special_diets['Count'].append(count)
cuisines = {}
for row in dataframe['Cuisines']:
    for cuisine in row.split(', '):
        if cuisine != 'no_data':
            if cuisine not in cuisines:
                cuisines[cuisine] = 0
            cuisines[cuisine] += 1
new_cuisines = {'Cuisine': [], 'Count': []}
for cuisine, count in cuisines.items():
    if count > 100:
        new_cuisines['Cuisine'].append(cuisine)
        new_cuisines['Count'].append(count)
fig, axs = plt.subplots(ncols=2, figsize=(16, 5))
axs[0].tick_params(axis='x', rotation=90)
axs[1].tick_params(axis='x', rotation=90)
sns.barplot(x="Diet", y="Count", data=pd.DataFrame(new_special_diets).sort_values(by=['Diet']),
            palette="Blues_d", ax=axs[0])
sns.barplot(x="Cuisine", y="Count", data=pd.DataFrame(new_cuisines).sort_values(by=['Count']),
            palette="Blues_d", ax=axs[1])
fig.savefig(Path.cwd().joinpath('restaurants', 'diets_and_cuisines.png'))

# Plot scatter
scatter_dataframe = dataframe.copy()
for column in ['Latitude', 'Longitude', 'Rating']:
    scatter_dataframe = scatter_dataframe[scatter_dataframe[column] != 'no_data']
    scatter_dataframe[column] = scatter_dataframe[column].astype(float)
scatter_dataframe = scatter_dataframe[(scatter_dataframe['Latitude'].between(59.8, 61) &
                                       scatter_dataframe['Longitude'].between(30, 31))]
fig, axs = plt.subplots(ncols=1, figsize=(15, 18))
sns.kdeplot(x='Longitude', y='Latitude',
            data=scatter_dataframe, cmap='Blues', shade=True, thresh=0.05, alpha=0.6, ax=axs)
sns.scatterplot(x="Longitude", y="Latitude",
                data=scatter_dataframe,
                palette="inferno",
                hue='Rating',
                size='Rating',
                legend='auto',
                ax=axs)
fig.savefig(Path.cwd().joinpath('restaurants', 'xy_scatter.png'))
