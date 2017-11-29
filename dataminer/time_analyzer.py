"""Term Analyzer (time_anlayzer.py)
Takes a directory of tweets and returns count time series of those tweets at
various temporal scales

Contributors:
Devin Gaffney & Ryan J. Gallagher
Network Science Institute, Northeastern University, 2017
"""

import os
import csv
import json
from collections import Counter

class Time_Analyzer:
    """
    Count the number of tweets for time series at various temporal scales

    Example:
        import time_analyzer
        time_analyzer.Time_Analyzer(parameters............)

    Parameters
    ----------
    tweet_dir: string
        Complete file path from working directory to directory of tweets

    working_dir: string, defaults to None
        Directory to build a directory of output files containing ranked lists
        of terms. If None, uses the user's current working directory

    Attributes
    ----------
    reduced_data: boolean
        True if working with tweets from summarized CSV file. False if working
        with the full JSON data.
    """

    def __init__(tweet_dir, working_dir=None):
        self.tweet_dir = tweet_dir
        self.got_top_terms = False
        if working_dir is None:
            self.working_dir = os.getcwd()
        else:
            self.working_dir = working_Dir
        if 'reduced' in self.tweet_dir:
            self.reduced_data = True
        else:
            self.reduced_data = False

    def get_timeline(self):
        # List out tweet files
        tweet_files = os.listdir(self.tweet_dir)
        # Get edges from each tweet file
        timeline = Counter()
        for filename in tweet_files:
            with open(self.tweet_dir+'/'+filename, 'rb') as f:
                # Open the file differently based on CSV or JSON
                if self.reduced_data is True:
                    tweet_file = self.a_most_dirty_hand(csv.reader(f, delimiter='\t'))
                else:
                    tweet_file = f
                # Read through each line of the file and update Counters
                for tweet in tweet_file:
                    try:
                        if self.reduced_data is True:
                            print tweet
                            text = unicode(tweet[9], 'utf-8')
                        else:
                            tweet = json.loads(line)
                            text = unicode(tweet['text'], 'utf-8')
