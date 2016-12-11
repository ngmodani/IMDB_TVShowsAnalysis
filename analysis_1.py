import argparse
#%matplotlib inline
import os,json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib as mpl
import matplotlib.pyplot as plt
np.random.seed(sum(map(ord, "aesthetics")))

# Taking user input
parser = argparse.ArgumentParser()
parser.add_argument("genre",type=str,help = "Enter the genre")
parser.add_argument("start_date",type = str,help = "Enter Min Premier Date of tv show (YYYY-MM-DD)")
parser.add_argument("end_date",type = str,help = "Enter Max Premier Date of tv show (YYYY-MM-DD)")
args = parser.parse_args()
#parsing user input
start_date = args.start_date
end_date = args.end_date
genre_select = args.genre

# function to convert json to dataFrame
def json_to_df_show(path):
    file = {}
    with open(path,'r') as f:
        file = json.load(f)
        f.close()
    df = json_normalize(file)
    return df

# Accessing all show.json from every folder
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
# changing datatype of column
df['premiered'] = pd.to_datetime(df['premiered'])
# creating dummy variables for all genres
df['genres']= df['genres'].apply(lambda x: '|'.join(x))
unique_genre = set()
for genre in df.genres.values :
    unique_genre.update(genre.split("|"))
for genre in unique_genre :
    df[genre]=0
for genre in unique_genre : 
    df.ix[df.ix[:,'genres'].str.contains(genre),genre] = 1

# error handling if loop
if genre_select in unique_genre:
    # extracting data for user inputted genre
    df_required = df[df[genre_select]==1]
    df_required = pd.concat([df_required.premiered,df_required.runtime],axis=1)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df_required.plot(x='premiered',y="runtime",ax=ax)
    ax.set_ylabel("Mins")
    ax.set_xlabel("Premier")
    # Taking care of date range user inputted
    ax.set_xlim([start_date, end_date]) 
    ax.set_title('Year-wise runtime of shows for "'+genre_select +'" genre')
    ax.set_autoscale_on(True)
    # making required directories
    if os.path.isdir("output/analysis_1")==False:
          os.mkdir("output/analysis_1")
    # save image of the plot
    file_name = "output/analysis_1/analysis_1_"+str(pd.datetime.now())+".png"
    fig.savefig(file_name)
    # saving CSV file
    csv_name = "output/analysis_1/analysis_1_"+str(pd.datetime.now())+".csv"
    df_required.to_csv(csv_name,sep=',',index=False)
else:
    # Error message in case of wrong input
    print("Invalid Genre. Please type from following options:")
    out_error = [print(x) for x in unique_genre if len(x)>1]

