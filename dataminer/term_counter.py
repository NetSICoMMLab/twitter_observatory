"""Term Counter (term_counter.py)
Takes a directory of tweets and ranks terms (hashtags, unigrams,n-grams,
phrases) in those tweets. Returns full text of tweets for tweets
containing the top terms (optional?)

Contributors:
Devin Gaffney & Ryan J. Gallagher
Network Science Institute, Northeastern University, 2017
"""
import os
import sys
import csv
import json
from datetime import datetime
from collections import Counter

from nltk.corpus import stopwords
from ttp import ttp
stop_words = stopwords.words('english')
from string import punctuation
exclude = set(punctuation)
exclude.remove('#')
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=False)
import codecs

class TermCounter:
    """
    Count top terms (hashtags, unigrams, n-grams, phrases) for a set of tweets

    Example:
        import term_counter
        term_counter.TermCounter(parameters............)

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
        if working_dir is None:
            self.working_dir = os.getcwd()
        else:
            self.working_dir = working_dir
        if 'reduced' in self.tweet_dir:
            self.reduced_data = True
        else:
            self.reduced_data = False

    def get_counts(self):
        output_dir = self.working_dir+'/term_counts'
        counts = {}
        for key in ["terms", "hashtags", "mentions", "urls"]:
            counts[key] = [r for r in self.a_most_dirty_hand(csv.reader(output_dir+"/"+key+".csv", delimiter='\t'))]
        return counts

    def get_ranked_terms(self, max_n=1):
        """
        Gets the top terms (currently: hashtags, unigrams) from a set
        of tweets

        INPUT
        -----
        max_n: int
            Integer specifiying max n-grams to retrieve

        OUTPUT
        ------
        Makes separate files containing ranked lists of terms
        """
        # List out tweet files
        tweet_files = os.listdir(self.tweet_dir)
        # Get hashtags and unigram counts from each file
        final_counts = {'terms': Counter(), 'hashtags': Counter(), 'mentions': Counter(), 'urls': Counter()}
        for filename in tweet_files:
            print filename
            file_counts = self.get_terms_from_file(filename, max_n)
            for key in file_counts.keys():
                final_counts[key].update(file_counts[key])
        # Output ranked counts to files
        output_dir = self.working_dir+'/term_counts'
        try:
            os.makedirs(output_dir)
        except:
            print "File '"+output_dir+"' exists"
        for key in final_counts.keys():
            self.write_ranked_list(final_counts[key], output_dir+'/'+key+'.csv')

    def get_terms_from_file(self, filename, max_n):
        """
        Extracts counts of terms and hashtags for all tweets in a tweet file.
        File currently extracts unigrams, as preprocessed by clean_tweet()

        OUTPUT
        ------
        term2count and hashtag2count, Counters
            Counter objects for terms and hashtags found in the file's tweets

        NOTE: term2count will include hashtags. However, there are instances
        where a hashtag does not fully appear in text (cut off for some reason?),
        but it fully appears in the hashtag field
        """
        term2count = Counter()
        hashtag2count = Counter()
        mention2count = Counter()
        url2count = Counter()
        null_rows = 0
        # Get hashtags and raw tweet text
        # this is kinda weird, you pass the filename to this func but assume where it is under tweet dir...
        # wrap the first part as a function (for use with get_full_text()) using f.open() and f.close() instead?
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
                        text = unicode(tweet[9], 'utf-8')
                    else:
                        tweet = json.loads(line)
                        text = unicode(tweet['text'], 'utf-8')
                    # Clean tweet text
                    clean_text = self.clean_tweet(text)
                    term2count.update(clean_text)
                    # Update Counters
                    hashtag2count.update(self.hashtags(text))
                    mention2count.update(self.mentions(text))
                    url2count.update(self.urls(text))
                except:
                    print "Null row."
                    null_rows += 1
        print str(null_rows)+" null rows encountered"
        return {'terms': term2count, 'hashtags': hashtag2count, 'mentions': mention2count, 'urls': url2count}

    def tweets_matching_tokens(self, top_count=20, types=["hashtags"], include_user_if_user_mentions=False):
        if "term_counts" in os.listdir(self.working_dir) and len(set(types)&set([el.replace(".csv", "") for el in os.listdir(self.working_dir+"/term_counts")])) == len(types):
            term_counts = Counter()
            for key in types:
                with open(self.working_dir+'/term_counts/'+key+'.csv', 'rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[1] not in term_counts.keys():
                            term_counts[row[1]] = int(row[2])
                        else:
                            term_counts[row[1]] += int(row[2])
            top_terms = [el[0] for el in term_counts.most_common(top_count)]
            tweet_files = os.listdir(self.tweet_dir)
            # Search through tweet files
            corpus = []
            for filename in tweet_files:
                print filename
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
                                text = unicode(tweet[9], 'utf-8')
                                screen_name = tweet[-1]
                            else:
                                tweet = json.loads(line)
                                text = unicode(tweet['text'], 'utf-8')
                                screen_name = tweet['screen_name']
                            for term in top_terms:
                                if term in text or (include_user_if_user_mentions == True and term == tweet[-1]):
                                    corpus.append(tweet)
                        except:
                            print "Null row."
                            null_rows += 1
            output_dir = self.working_dir+'/top_term_tweets'
            try:
                os.makedirs(output_dir)
            except:
                print "File '"+output_dir+"' exists"
            if include_user_if_user_mentions == True:
                filename = output_dir+"/top_mentioned_users_timeline.csv"
            else:
                filename = output_dir+"/top_term_tweets.csv"
            with open(filename, 'a') as f:
                csvwriter = csv.writer(f, delimiter=',')
                csvwriter.writerows(corpus)
        else:
            print "Cannot run this until you've run get_ranked_terms to generate term counts!!"
            sys.exit()

    # --------------------------------------------------------------------------
    # ---------------------------- Helper functions ----------------------------
    # --------------------------------------------------------------------------
    def clean_tweet(self, tweet_text):
        """
        Cleans tweet text for extracting unigrams. Steps for cleaning:
        1. Tokenize text using NLTK tweet tokenizer
            a. Remove handles
            b. Tokenize tweet
            c. Lowercase unigrams (except emoticons)
        2. Do basic filtering of 'rt' and URLs from tweet (not extensive)
        3. Remove stop words from tweet (NLTK stop word list)
        4. Remove punctuation from tweet, except hashtag (#) symbol

        TODO: this func doesn't play well with wanting to get n-grams or phrases

        OUTPUT
        ------
        cleaned_text, list of strings
            List of unigrams from tweet following above processing steps
        """
        # Tokenize the tweet text using NLTK
        tokenized_text = tknzr.tokenize(tweet_text)
        # Remove 'rt', links, stop words
        filtered_text = [gram for gram in tokenized_text if (gram != 'rt')
                        and ('http' not in gram) and ('//t.co' not in gram)
                        and (gram not in stop_words)]
        # Join text to one string, remove punctuation, join back to list
        text = ' '.join(filtered_text)
        text_chars_noPunct = [char for char in text if char not in exclude]
        text_noPunct = "".join(text_chars_noPunct)
        # Split back to list of words
        cleaned_text = text_noPunct.strip().split()
        return cleaned_text

    def parse(self, text):
        return ttp.Parser().parse(text)

    def hashtags(self, text):
        return self.parse(text).tags

    def mentions(self, text):
        return self.parse(text).users

    def urls(self, text):
        return self.parse(text).urls

    def write_ranked_list(self, key2value, filename):
        """
        Expects a dict where values are counts
        Writes file (CSV file) of terms, counts, and rank
        """
        # Dict -> sorted list of (value, key) pairs in high->low order
        values_keys = [(key2value[key], key) for key in key2value.keys()]
        values_keys.sort(reverse = True)
        # Write ranks, keys, and values, to file
        with open(filename, 'a') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for k,(value,key) in enumerate(values_keys):
                csvwriter.writerow([k,unicode(key).encode("utf-8"),value])
    
    def a_most_dirty_hand(self, csv_reader):
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                # error handling what you want.
                pass
            continue
        return
