
import seaborn as sns
import os,json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib as mpl
import matplotlib.pyplot as plt

# function to convert json to dataFrame
def json_to_df_show(show_path):
    file = {}
    with open(show_path,'r') as f:
        file = json.load(f)
        f.close()
    df = json_normalize(file)
    return df
# function to read all episode.json & count avg. no of episodes (counting for every season)
def get_ep_count(ep_path):
    ep = {}
    with open(ep_path,'r') as f:
        ep = json.load(f)
        f.close()
    ep_list = []
    for episode in ep:
        record = []
        record.append(episode['season'])
        ep_list.append(record)
    df_ep = pd.DataFrame(ep_list,columns=["season"])
    return df_ep.season.value_counts().values.mean()
    
# Accessing all tv_shows
folders = [x[0] for x in os.walk("data/tv_shows/")]
# creating empty DF
df = pd.DataFrame()
ep_list = []
# Converting all show.json's to one DF after reading their average episode count per season
for paths in folders[1:]:
    show_path = paths+"/show.json"
    df_temp = json_to_df_show(show_path)
    ep_path = paths+"/episodes.json"
    ep_list.append(round(get_ep_count(ep_path),0))
    df = pd.concat([df,df_temp],axis=0)
df['ep_count'] = ep_list

# reindexing
df.index = range(len(df))
# delisting genres to string separated by "|"
df['genres']= df['genres'].apply(lambda x: '|'.join(x))
unique_genre = set()
for genre in df.genres.values :
    unique_genre.update(genre.split("|"))
unique_genre.remove("")
all_genre = list(unique_genre)

df_analysis_4 = pd.concat([df.genres,df.ep_count,df['rating.average'].dropna()],axis=1)
df_analysis_4 = df_analysis_4[df_analysis_4.genres!=""]
unique_genre = set(all_genre)
# Preprocessing complete , Analysing the data now
genre_wise = []
while unique_genre:
    genr = unique_genre.pop()
    record=[]
    record.append(genr)
    avg_ep = df_analysis_4[df_analysis_4.genres.str.contains(genr)]['ep_count'].mean()
    record.append(round(avg_ep,0))
    avg_rating = df_analysis_4[df_analysis_4.genres.str.contains(genr)]['rating.average'].mean()
    record.append(float("{0:.1f}".format(avg_rating)))
    genre_wise.append(record)

# Final Data
df_gw = pd.DataFrame(genre_wise,columns=["Genre","Avg_Episodes","Avg_Rating"])
# Plotting chart
plt.subplots(figsize=(10,5))
ax = sns.barplot(x="Genre",y="Avg_Episodes",data=df_gw,color='c')
ax.set_title('Avg. No. of Episodes per season for each Genre')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
ax.xaxis.get_label().set_fontsize(20)
ax.yaxis.get_label().set_fontsize(20)
ax.title.set_fontsize(25)
ax.tick_params(axis='x', which='major',labelsize=13)
ax.tick_params(axis='y', which='major',labelsize=15)
ax.set_ylabel("No. of Episodes")

# making the reqd. directory
if os.path.isdir("output/analysis_4")==False:
    os.mkdir("output/analysis_4")
# saving the graph
file_name = "output/analysis_4/analysis_4_"+str(pd.datetime.now())+".png"
fig = ax.get_figure()
fig.savefig(file_name)
# Saving CSV file
csv_name = "output/analysis_4/analysis_4_"+str(pd.datetime.now())+".csv"
df_gw.to_csv(csv_name,sep=',',index=False)

