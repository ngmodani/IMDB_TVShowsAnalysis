# IMDB top 250 TV Shows Analysis

This repository shows python based data analysis of Most Popular TV Shows (as determined by IMDb Users).
The list of top 250 TV shows is scraped from [IMDB](http://www.imdb.com/chart/toptv/) and the data about each show and their respective episodes and cast is pulled from [TV Maze API](http://www.tvmaze.com/api). 

The theme of all analysis performed is focussed on how a new show-maker (producer) can learn from previous highly successful TV Shows. This will enable him/her to decide what kind of show should be produced to be successful.

*Note: All code is written in Python3+.*

## How the data is collected

```
python collect_data.py
```
This script first scrapes the data from [IMDB top 250 TV shows](http://www.imdb.com/chart/toptv/) and then downloads and organizes the data from [TVMaze](http://www.tvmaze.com/api) in local file system. All the data pulled is in JSON format.

*Note: API call restriction is being already being taken care in script*

## Analysis

### Trend of runtime (air time per episode) of shows for a given Genre & specific date range
```
python analysis_1.py Comedy 2008-01-01 2016-01-01
```
This script takes in 3 inputs :
* Genre
* Start Date (YYYY-MM-DD)
* End Date (YYYY-MM-DD)

One major question for a producer, from financial point of view in today's competitive time, is to get air time on TV because every minute of broadast costs fortune.
This analysis will shows a trend of how the length of episodes have changed over the years and can help in deciding air time for any running or new show.
![Fig 1](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_1.jpg)

### Genre wise Rating for a given Language
```
python analysis_2.py English
```
This script takes in 1 input :
* Language
For any producer, <b>Genre</b> is the most important choice to make a TV show. This script shows how for any specific language which genre would be best to work on.
![Fig2](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_2.jpg)

### Size of Cast 
```
python analysis_3.py
```
To make a show, size of cast varies for every type of story. This analysis helps to decide what can be the size of his cast on the basis of Genre and type of broadcast his show can have.
![Fig3](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_3.jpg)

### Length of a Season
```
python analysis_4.py
```
TV shows always had and will always have their makig every year i.e. season-wise. This analysis helps to decide what can be the length of a season for a Genre.
![Fig4](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_4.jpg)

### Summary of Top Shows
```
python analysis_5.py
```
Other than above specific questions. There are many other decisions to be made by a producer.
* Broadcasting Properties of current TV shows
This answers what type of channel and on what days of week show can be broadcasted.
![Fig5a](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_5_broadcst.jpg)

* Distribution by Country, Language & Category of shows
This answers what type of show & languauge & country of broadcast can be for the show.
![Fig5b](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_5_distribution.jpg)

* Status of The shows
A good show is one which stops in time and this analysis tells the same.
![Fig5c](https://github.com/ngmodani/IMDB_TVShowsAnalysis/blob/master/data/images/analysis_5_stat.jpg)

### Credits

Use of the TVmaze API is licensed by [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)
