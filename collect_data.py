from bs4 import BeautifulSoup
import json
import os
import time
import requests

# get IMDB top 250 TV shows
imdb_page = requests.get("http://www.imdb.com/chart/toptv/")
html_doc = imdb_page.text
soup = BeautifulSoup(html_doc, 'html.parser')
# extract imdb ID of top 250 TV shows
tv_show_imdb_ids = []
for link in soup.find_all('a'):
    href = link.get('href')
    if str(href).startswith("/title/tt"):
        get_imdb_id = href.split('/')
        tv_show_imdb_ids.append(get_imdb_id[2])
# list of unique IMDB IDs
tv_show_imdb_ids = list(set(tv_show_imdb_ids))

# Creating base directories
if os.path.isdir("data")==False:
    os.mkdir("data")
if os.path.isdir("data/tv_shows")==False:
    os.mkdir("data/tv_shows")
if os.path.isdir("output")==False:
    os.mkdir("output")

count = 0
for imdb_id in tv_show_imdb_ids:
    payload={}
    payload['imdb']=imdb_id
    tv_show_response = requests.get("http://api.tvmaze.com/lookup/shows",params=payload)
    if count < 17:
        if tv_show_response.ok:
            tv_show_response = tv_show_response.json()
            show_id = tv_show_response['id']
            #show_name = tv_show_response['name']
            show_url = tv_show_response['url']
            url = show_url.split("/")
            show_name = url[-1]
            file_name = "data/tv_shows/"+str(show_id)+"_"+show_name
            os.mkdir(file_name)
            # creating json file for show
            with open(file_name+"/show.json",'w') as f:
                json.dump(tv_show_response,f)
                f.close()
            # fetching & creating json file for show's cast
            url_cast = "http://api.tvmaze.com/shows/"+str(show_id)+"/cast"
            cast_json_response = requests.get(url_cast)
            cast_json_response = cast_json_response.json() 
            with open(file_name+"/cast.json",'w') as f:
                json.dump(cast_json_response,f)
                f.close()
            # fetching & creating json file for show's episodes
            url_epsiode = "http://api.tvmaze.com/shows/"+str(show_id)+"/episodes"
            episode_json_response = requests.get(url_epsiode)
            episode_json_response = episode_json_response.json()
            with open(file_name+"/episodes.json",'w') as f:
                json.dump(episode_json_response,f)
                f.close()
            count = count + 3
    else:
        count = 0
        # API call is limited to 20 calls per 10 sec so using sleep
        time.sleep(10)
        