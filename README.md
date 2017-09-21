# CoMM Lab Tweet Dataminer
A suite of scripts to automate collection and analysis of tweets from the Twitter Gardenhose at Northeastern University. Currently, a user can specify a keyword or hashtag. More complex queries are left for future work.

**Contributors:** Devin Gaffney, Ryan J. Gallagher

## extractor.py
Searches the Gardenhose (either the full JSON files or summarized CSV files) based on a keyword or set of keywords and outputs matches for later analysis. The extractor supports "AND" queries (search looks for *all* hashtags to appear in each tweet) or "OR" queries (search looks individually for each hashtag in tweets).

Sample call:

## term_counter.py
TODO:
- Counts the hashtags appearing in the tweets
- Returns full text of tweets for tweets containing the top *n* hashtags
- Counts the n-grams appearing in the tweets
- Builds a doc-term matrix?
- Sentiment analysis? (probably should be in different script around NLP tasks)

## timeline.py
TODO:
- Returns time series of tweets at various temporal scales

## network.py
TODO:
- Makes a edge lists based on Twitter interactions (user-specified AND/OR: retweets, mentions, quote-retweets)
- Counts number of nodes and edges
- Creates the in-degree distribution (more broadly, ranks users by any network metric) and returns the full text of tweets by or mentioning the top n users in this distribution
- Centrality?
- Mesoscale structures?

# learner
TODO:
- Suite of classifiers to try and infer gender, race, etc for later qualitative analysis
