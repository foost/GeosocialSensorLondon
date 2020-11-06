# GeosocialSensorLondon

This repository contains materials to reproduce and replicate an analysis on using geosocial sensors. 

List of files and brief description:

*TwitterStreamingAPI_London.py*

Python script used to retrieve Tweets

*FlickrSearchAPI_London.py*

Python script used to retrieve Flickr image meta data

*TwitterBuildTermVectors.py*

Python script used to parse Tweets for terms found in terms_stemmed.txt

*FlickrBuildTermVectors.py*

Python script used to parse Tweets for terms found in terms_stemmed.txt

*Flickr_IDs.zip*

CSV file with IDs of all Flickr images used as input data

*Tweet_IDs.zip*

CSV file with IDs of all Tweets used as input data

*bots_identification.sql*

SQL statements used to determine which Tweets are likely to be from bots (and excluded from further analysis)

*TF-IDF_computation.ipynb*

Python Jupyter notebook which computes TF-IDF scores

*TF-IDF_analysis.ipynb*

Python Jupyter notebook which analyses the TF-IDF scores and socio-demographics

*/**.npy*

several files containing intermediary results (numpy arrays of the TF-IDF scores)

*Flickr/**.csv and Twitter/**.csv*

several files containing results of the TF-IDF scores analysis

*sentiment_conputation.ipynb*

Python Jupyter notebook which computes sentiment scores

*vaderSentiment_mod.py*

modified VADER sentiment anlyzer (see https://github.com/cjhutto/vaderSentiment/issues/99 and paper for details)

*sentiment_analysis.ipynb*

Python Jupyter notebook which analysis the sentiments and socio-demographics

*sentiments_groups_wards.csv*

results for sentiments and LOAC groups at ward level

*sentiments_sociodem_msoa.csv*

results for sentiments and socio-demographics at MSOA level

*spatial_temporal_analysis.ipynb*

Jupyter Python notebook which analysis sentiments for spatial pattern and changes over time

