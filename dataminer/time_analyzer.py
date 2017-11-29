"""Time Analyzer (time_anlayzer.py)
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
from dateutil import parser
import datetime

class TimeAnalyzer:
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
    def __init__(self, tweet_dir, working_dir=None):
        self.tweet_dir = tweet_dir
        self.got_top_terms = False
        if working_dir is None:
            self.working_dir = os.getcwd()
        else:
            self.working_dir = working_dir
        if 'reduced' in self.tweet_dir:
            self.reduced_data = True
        else:
            self.reduced_data = False
    
    def get_timeline(self):
        # List out tweet files
        tweet_files = os.listdir(self.tweet_dir)
        null_rows = 0
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
                            timeline.update([parser.parse(tweet[2]).strftime("%Y-%m-%d")])
                        else:
                            tweet = json.loads(line)
                            timeline.update([parser.parse(tweet["created_at"]).strftime("%Y-%m-%d")])
                    except:
                        print "Null row."
                        null_rows += 1
        return timeline

    def write_timelines(self):
        timeline = self.get_timeline()
        earliest = sorted(timeline.keys())[0]
        latest = sorted(timeline.keys())[-1]
        time_cursor = parser.parse(earliest)
        end_time = parser.parse(latest)
        cumulative = []
        spiked = []
        cumulative_count = 0
        while time_cursor <= end_time:
            time_str = time_cursor.strftime("%Y-%m-%d")
            this_count = 0
            if time_str in timeline.keys():
                cumulative_count += timeline[time_str]
                this_count = timeline[time_str]
            cumulative.append([time_str, cumulative_count])
            spiked.append([time_str, this_count])
            time_cursor = time_cursor+datetime.timedelta(days=1)
        try:
            os.makedirs(output_dir)
        except:
            print "File '"+output_dir+"' exists"
        spiked_filename = self.working_dir+'/timelines'+"/spiked.csv"
        cumulative_filename = self.working_dir+'/timelines'+"/cumulative.csv"
        with open(spiked_filename, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerows(spiked)
        with open(cumulative_filename, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerows(cumulative)

        
    def a_most_dirty_hand(self, csv_reader):
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                # error handling what you want.
                pass
            continue
        return
