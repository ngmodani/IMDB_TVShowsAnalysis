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
# function to read cast.json file & count cast members of a show
def get_cast_count(cast_path):
    cast = {}
    with open(cast_path,'r') as f_c:
        cast = json.load(f_c)
        f_c.close()
    return len(cast)
    
# Accessing all tv_shows folder
folders = [x[0] for x in os.walk("data/tv_shows/")]
# creating empty DF
df = pd.DataFrame()
cast_list = []
# Converting all show.json's to one DF and appending their cast count
for paths in folders[1:]:
    show_path = paths+"/show.json"
    df_temp = json_to_df_show(show_path)
    cast_path = paths+"/cast.json"
    cast_list.append(get_cast_count(cast_path))
    df = pd.concat([df,df_temp],axis=0)
df['cast_count'] = cast_list

# reindexing
df.index = range(len(df))
# Extracting channel type Web or TV
channel_type = []
for network in  df['webChannel.name']:
    if type(network) == type("check"):
        channel_type.append("Web")
    else:
        channel_type.append("TV")
df['channel_type'] = channel_type

df_analysis_3 = pd.concat([df.genres,df.cast_count,df.channel_type],axis=1)
# delisting genres to string separated by "|"
df_analysis_3['genres']= df_analysis_3['genres'].apply(lambda x: '|'.join(x))
unique_genre = set()
# making a set of unique genres
for genre in df_analysis_3.genres.values :
    unique_genre.update(genre.split("|"))


# removing empty rows
df_analysis_3 = df_analysis_3[df_analysis_3.genres!=""]
unique_genre.remove("")
all_genre = list(unique_genre)
df_web = df_analysis_3[df_analysis_3.channel_type=='Web']
df_tv = df_analysis_3[df_analysis_3.channel_type=='TV']

# calculating Average genre wise cast count for 
genre_wise = []
while unique_genre:
    genr = unique_genre.pop()
    record=[]
    record.append(genr)
    record.append(df_web[df_web.genres.str.contains(genr)]['cast_count'].mean())
    record.append("Web")
    genre_wise.append(record)

unique_genre = set(all_genre)
while unique_genre:
    genr = unique_genre.pop()
    record=[]
    record.append(genr)
    record.append(df_tv[df_tv.genres.str.contains(genr)]['cast_count'].mean())
    record.append("TV")
    genre_wise.append(record)

df_genre_wise = pd.DataFrame(genre_wise,columns=["Genre","cast_count","channel_type"]).dropna()

# Plotting
plt.subplots(figsize=(10,8))
ax = sns.barplot(y=("cast_count"),x="Genre",hue="channel_type",data=df_genre_wise)
ax.set_title('Number of Cast Members for TV shows by Genre ')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
ax.xaxis.get_label().set_fontsize(20)
ax.yaxis.get_label().set_fontsize(20)
ax.title.set_fontsize(25)
ax.tick_params(axis='x', which='major',labelsize=12)
ax.tick_params(axis='y', which='major',labelsize=15)
#ax.set_ylim(7,10)
ax.set_ylabel("Avg. Cast Members")
plt.legend(loc=0,title="Channel Type")
# making the reqd. directory
if os.path.isdir("output/analysis_3")==False:
    os.mkdir("output/analysis_3")
# saving the graph
file_name = "output/analysis_3/analysis_3_"+str(pd.datetime.now())+".png"
fig = ax.get_figure()
fig.savefig(file_name)
# saving CSV file
csv_name = "output/analysis_3/analysis_3_"+str(pd.datetime.now())+".csv"
df_genre_wise.to_csv(csv_name,sep=',',index=False)
