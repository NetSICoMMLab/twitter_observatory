# CoMM Lab Tweet Dataminer
A suite of scripts to automate collection and analysis of tweets from the Twitter Gardenhose at Northeastern University. Currently, a user can specify a keyword or hashtag. More complex queries are left for future work.

**Contributors:** Devin Gaffney & Ryan J. Gallagher, Northeastern University, 2017


## extractor.py
Extracts tweets from the Gardenhose (either from the full JSON files or
summarized CSV files) based on a keyword or set of keywords and outputs matched
tweets for later analysis. User can search for several keywords/hashtags
individually or search for tweets containing *all* of the specified keywords.

## term_counter.py
TODO: (extra)
- Counts the n-grams appearing in the tweets
- Builds a doc-term matrix?
- Sentiment analysis? (probably should be in different script around NLP tasks)

## timeline.py
TODO:
- Returns time series of tweets at various temporal scales

## network.py
TODO:
- Return the full text of tweets by or mentioning the top n users in this distribution (can we use term_counter for this?)

TODO: (extra)
- Let user specify what interactions they want (retweet, quote retweet, mention, reply)
- Rank users by any network measure
- Centrality?
- Mesoscale structures?

# learner
TODO:
- Suite of classifiers to try and infer gender, race, etc for later qualitative analysis


## installation instructions
pip install nltk
pip install twitter-text-python
python && `nltk.download("stopwords")`  

TODO: wrap all "analyzer" classes into one file so you don't have to import a whole bunch of different files
## example code
```python
from extractor import Extractor
gg = Extractor(["#AltonSterling"], "OR", "2014-02-01", "2016-02-01")

import term_counter
tc = term_counter.TermCounter("/home/dgaffney/hashtag_extractions/#AltonSterling_2015-08-09_2017-08-09_reduced", "/home/dgaffney/hashtag_results/#AltonSterling_2015-08-09_2017-08-09_reduced")
tc.get_ranked_terms()
tc.tweets_matching_tokens()

import network_analyzer
na = network_analyzer.NetworkAnalyzer("/home/dgaffney/hashtag_extractions/#AltonSterling_2015-08-09_2017-08-09_reduced", "/home/dgaffney/hashtag_results/#AltonSterling_2015-08-09_2017-08-09_reduced")
na.get_edge_list()
na.get_ranked_in_degree()
```
