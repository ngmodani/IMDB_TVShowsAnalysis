import argparse
#%matplotlib inline
import seaborn as sns
import os,json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib as mpl
import matplotlib.pyplot as plt

sns.set(style="whitegrid", color_codes=True)
np.random.seed(sum(map(ord, "categorical")))

# Taking user input
parser = argparse.ArgumentParser()
parser.add_argument("language",type=str,help = "Enter language")
args = parser.parse_args()
#parsing user input
language_select = args.language
# function to convert json to dataFrame
def json_to_df_show(path):
    file = {}
    with open(path,'r') as f:
        file = json.load(f)
        f.close()
    df = json_normalize(file)
    return df

# Accessing all tv_shows
folders = [x[0] for x in os.walk("data/tv_shows/")]
# creating empty DF
df = pd.DataFrame()
# Converting all jsons to one DF
for paths in folders[1:]:
    path = paths+"/show.json"
    df_temp = json_to_df_show(path)
    df = pd.concat([df,df_temp],axis=0)

# reindexing
df.index = range(len(df))
# checking by if-loop, whether user input correct or not
unique_lang = set(df.language.values)
if language_select in unique_lang:
       # creating dummy variables for all genres
       df['genres']= df['genres'].apply(lambda x: '|'.join(x))
       unique_genre = set()
       for genre in df.genres.values :
           unique_genre.update(genre.split("|"))

       # pre-processing useful columns for analysis
       df_analysis_2 = pd.concat([df.genres,df['rating.average'],df.language],axis=1)
       # selecting data only for user inputted language
       df_analysis_2 = df_analysis_2[df_analysis_2.language==language_select]
       df_analysis_2 = df_analysis_2[df_analysis_2.genres!=""]
       df_analysis_2 = df_analysis_2[df_analysis_2['rating.average'].notnull()]
       del df_analysis_2['language']
       unique_genre.remove("")
       genre_wise =[]
       # calculating Genre wise rating
       while unique_genre:
           genr = unique_genre.pop()
           record=[]
           record.append(genr)
           record.append(df_analysis_2[df_analysis_2.genres.str.contains(genr)]['rating.average'].mean())
           genre_wise.append(record)

       df_genre_wise = pd.DataFrame(genre_wise,columns=["Genre","Rating"])
       df_genre_wise = df_genre_wise[df_genre_wise.Rating.notnull()]
       # Plotting the graph 
       plt.subplots(figsize=(15,10))
       ax = sns.barplot(x="Genre",y="Rating",data=df_genre_wise,color='m')
       ax.set_title('Ratings of "'+language_select+'" TV shows by Genre')
       plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
       ax.xaxis.get_label().set_fontsize(25)
       ax.yaxis.get_label().set_fontsize(25)
       ax.title.set_fontsize(30)
       ax.tick_params(axis='x', which='major',labelsize=18)
       ax.tick_params(axis='y', which='major',labelsize=20)
       ax.set_ylim(7,10)
       ax.set_ylabel("Avg. Rating")
       # making the folder
       if os.path.isdir("output/analysis_2")==False:
          os.mkdir("output/analysis_2")
      # saving the graph
       file_name = "output/analysis_2/analysis_2_"+str(pd.datetime.now())+".png"
       fig = ax.get_figure()
       fig.savefig(file_name)
       #fig.savefig('data/images/analysis_2.jpg')
       csv_name = "output/analysis_2/analysis_2_"+str(pd.datetime.now())+".csv"
       df_genre_wise.to_csv(csv_name,sep=',',index=False)
else:
       print("Invalid language. Please type from following options:")
       out_error = [print(x) for x in unique_lang]
