import seaborn as sns
import os,json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *

def json_to_df_show(path):
    file = {}
    with open(path,'r') as f:
        file = json.load(f)
        f.close()
    df = json_normalize(file)
    return df

#test = os.walk("data/tv_shows")
folders = [x[0] for x in os.walk("data/tv_shows/")]
df = pd.DataFrame()
for paths in folders[1:]:
    path = paths+"/show.json"
    df_temp = json_to_df_show(path)
    df = pd.concat([df,df_temp],axis=0)
# deleting unwanted columns
del df['_links.nextepisode.href']
del df['network.id']
del df['webChannel.id']
del df['weight']
del df['network']
del df['webChannel']
del df['_links.previousepisode.href']
del df['_links.self.href']
del df['externals.imdb']
del df['externals.thetvdb']
del df['externals.tvrage']
del df['image.medium']
del df['image.original']
del df['url']
del df['summary']
del df['webChannel.country.timezone']
del df['network.country.timezone']
del df['updated']
# reindexing
df.index = range(len(df))

# extracting scheduled days and Weekend or not
df_days = pd.DataFrame(df['schedule.days'].tolist(),)
no_of_days =[]
for days in df['schedule.days']:
    record = []
    record.append(len(days))
    if "Sunday" in days or "Saturday" in days:
        record.append("True")
    else:
        record.append("False")
    no_of_days.append(record)
# making it a dataframe and appending to original DF
df_days_new = pd.DataFrame(no_of_days,columns=["Weekly_Frequency","on_Weekend"])
df = pd.concat([df,df_days_new],axis=1)
del df['schedule.days']

# extracting channels and countries and web or not
df_network = pd.concat([df['network.country.code'],df['network.country.name'],
                        df['network.name'],df['webChannel.country.code'],
                        df['webChannel.country.name'],df['webChannel.name']],axis = 1)

df_network['channel_name']=pd.concat([df['network.name'].dropna(), df['webChannel.name'].dropna()]).reindex_like(df)
df_network['country_name']=pd.concat([df['network.country.name'].dropna(), df['webChannel.country.name'].dropna()]).reindex_like(df)
df_network['country_code']=pd.concat([df['network.country.code'].dropna(), df['webChannel.country.code'].dropna()]).reindex_like(df)

isWebChannel = []
for network in  df['network.name']:
    if type(network) == type("check"):
        isWebChannel.append("False")
    else:
        isWebChannel.append("True")

df_isWeb = pd.DataFrame(isWebChannel,columns=["isWebChannel"])
df_network = pd.concat([df_network,df_isWeb],axis=1)
del df_network['network.country.code']
del df_network['network.country.name']
del df_network['network.name']
del df_network['webChannel.country.code']
del df_network['webChannel.country.name']
del df_network['webChannel.name']
# appending the columns to df
df = pd.concat([df,df_network],axis=1)
# deleting processed columns
del df['network.country.code']
del df['network.country.name']
del df['network.name']
del df['webChannel.country.code']
del df['webChannel.country.name']
del df['webChannel.name']
# deleting more unwanted columns
del df['genres']
del df['id']
del df['name']
del df['rating.average']
del df['runtime']
del df['schedule.time']
del df['premiered']

# Status of shows
df_status = pd.DataFrame(df.status.value_counts()).reset_index()
df_status.columns = ['Status','Count']
# Type of Show
df_type = pd.DataFrame(df.type.value_counts()).reset_index()
df_type.columns=['Type','Count']
# Broadcasts on Weekend or not
df_weekend = pd.DataFrame(df.on_Weekend.value_counts()).reset_index()
df_weekend.columns=['Weekend','Count']
# Broadcasts on Web or not
df_web = pd.DataFrame(df.isWebChannel.value_counts()).reset_index()
df_web.columns=['Channel_type','Count']
# Primary Country of Broadcast
df_country  = pd.DataFrame(df.country_name.value_counts()).reset_index()
df_country.columns=['Country','Count']
# Language of the show
df_lang  = pd.DataFrame(df.language.value_counts()).reset_index()
df_lang.columns=['Language','Count']

# Plotting show status
sns.set_context('notebook',font_scale=1.5)
# Data to plot
labels = df_status.Status.tolist()
sizes = df_status.Count.tolist()
colors = ['yellowgreen', 'green','yellow']
explode = [0.1,0,0.1]

# making the directory
if not os.path.isdir("output/analysis_5"):
    os.mkdir("output/analysis_5")

#Create figure and axis
fg,ax = plt.subplots(1,1,figsize=(25,12),sharex=True)
ax.pie(sizes, labels=labels, colors=colors, shadow=True, explode=explode,autopct='%1.1f%%', startangle=90, radius=0.40)
ax.set_title('Current Status of Top Shows')
#plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig("output/analysis_5/analysis_5_status_"+str(pd.datetime.now())+".png", bbox_inches='tight')

csv_name = "output/analysis_5/analysis_5_status_"+str(pd.datetime.now())+".csv"
df_status.to_csv(csv_name,sep=',',index=False)

# Plotting show weekend or not & channel_type
# Data to plot
label_w = df_weekend.Weekend.tolist()
size_w = df_weekend.Count.tolist()
label_c = df_web.Channel_type.tolist()
size_c = df_web.Count.tolist()
colors = ['cyan','blue']
explode = [0.1,0.1]

#Create figure and axis
fg,ax = plt.subplots(1,2,figsize=(12,12),sharex=True)
ax[0].pie(size_w, labels=label_w, colors=colors, shadow=True, explode=explode, autopct='%1.1f%%', startangle=90, radius=0.40)
ax[0].set_title('% of Shows Broadcasted on Weekend')
ax[1].pie(size_c, labels=label_c, colors=colors, shadow=True, explode=explode, autopct='%1.1f%%', startangle=90, radius=0.40)
ax[1].set_title('% of Shows Broadcasted on Web')
#plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig("output/analysis_5/analysis_5_broadcast_"+str(pd.datetime.now())+".png", bbox_inches='tight')

csv_name = "output/analysis_5/analysis_5_broadcast_web_"+str(pd.datetime.now())+".csv"
df_web.to_csv(csv_name,sep=',',index=False)

csv_name = "output/analysis_5/analysis_5_broadcast_weekend_"+str(pd.datetime.now())+".csv"
df_weekend.to_csv(csv_name,sep=',',index=False)

fg, (ax1, ax2,ax3) = plt.subplots(ncols=3, sharey=True)

# Plotting chart for Countries
sns.barplot(x="Country",y="Count",data=df_country,color='cyan',ax=ax1)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
ax1.xaxis.get_label().set_fontsize(20)
ax1.yaxis.get_label().set_fontsize(20)
ax1.title.set_fontsize(25)
ax1.tick_params(axis='x', which='major',labelsize=10)
ax1.tick_params(axis='y', which='major',labelsize=15)
ax1.set_ylabel("Count")

# Plotting chart for Languages
sns.barplot(x="Language",y="Count",data=df_lang,color='pink',ax=ax2)
ax2.set_title("Distribution of Top TV shows")
#ax2.set_title('Language-wise Distribution')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
ax2.xaxis.get_label().set_fontsize(20)
ax2.yaxis.get_label().set_fontsize(20)
ax2.title.set_fontsize(25)
ax2.tick_params(axis='x', which='major',labelsize=10)
ax2.tick_params(axis='y', which='major',labelsize=15)
ax2.set_ylabel("Count")

# Plotting chart for Category
sns.barplot(x="Type",y="Count",data=df_type,color='y',ax=ax3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
ax3.xaxis.get_label().set_fontsize(20)
ax3.yaxis.get_label().set_fontsize(20)
ax3.title.set_fontsize(25)
ax3.tick_params(axis='x', which='major',labelsize=10)
ax3.tick_params(axis='y', which='major',labelsize=15)
ax3.set_ylabel("Count")
ax3.set_xlabel("Category")

fg.savefig("output/analysis_5/analysis_5_distribution_"+str(pd.datetime.now())+".png", bbox_inches='tight')

csv_name = "output/analysis_5/analysis_5_distribution_country_"+str(pd.datetime.now())+".csv"
df_country.to_csv(csv_name,sep=',',index=False)

csv_name = "output/analysis_5/analysis_5_distribution_lang_"+str(pd.datetime.now())+".csv"
df_lang.to_csv(csv_name,sep=',',index=False)

csv_name = "output/analysis_5/analysis_5_distribution_category_"+str(pd.datetime.now())+".csv"
df_type.to_csv(csv_name,sep=',',index=False)

