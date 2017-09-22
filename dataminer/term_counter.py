"""Term Counter (term_counter.py)
Takes a directory of tweets and ranks terms (hashtags, unigrams,n-grams,
phrases) in those tweets. Returns full text of tweets for tweets
containing the top terms (optional?)

Contributors:
Devin Gaffney & Ryan J. Gallagher
Network Science Institute, Northeastern University, 2017
"""
import os
import csv
import json
from datetime import datetime
from collections import Counter

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from string import punctuation
exclude = set(punctuation)
exclude.remove('#')
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=False)


class Term_Counter:
    """
    Count top terms (hashtags, unigrams, n-grams, phrases) for a set of tweets

    Example:
        import term_counter
        term_counter.Term_Counter()

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


    def get_top_terms(self, max_n=1):
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
        #TODO: extend to n-grams and phrases. Need to be more careful about
        #      clean_tweet() if you do this

        # List out tweet files
        tweet_files = os.listdir(self.tweet_dir)
        # Get hashtags and unigram counts from each file
        term2count = Counter()
        hashtag2count = Counter()
        for filename in tweet_files:
            term_counts,hashtag_counts = self.get_top_terms_from_file(filename, max_n)
            term2count.update(term_counts)
            hashtag2count.update(hashtag_counts)
        # Output ranked counts to files
        output_dir = self.working_dir+'/term_counts'
        write_ranked_list(term2count, output_dir+'/'+'unigrams.csv'))
        write_ranked_list(hashtag2count, output_dir+'/'+'hashtags.csv')

    def get_top_terms_from_file(self, filename, max_n):
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
        # Get hashtags and raw tweet text
        with open(tweet_dir+'/'+filename, 'rb') as f:
            # Open the file differently based on CSV or JSON
            if self.reduced_data is True:
                # TODO: what is the proper delimiter?
                tweet_file = csv.reader(f, delimiter=',')
            else:
                tweet_file = f
            # Read through each line of the file and update Counters
            for tweet in tweet_file:
                if self.reduced_data is True:
                    #TODO: figure out proper indices of row
                    text = tweet[]
                    hashtags = tweet[]
                else:
                    tweet = json.loads(line)
                    #TODO: figure out proper keys of dict
                    text = tweet['text']
                    hashtags = tweet[][]
                # Clean tweet text
                clean_text = clean_tweet(text)
                # Update Counters
                term2count.update(clean_text)
                hashtag2count.update(hashtags)

        return (term2count, hashtag2count)




    def get_full_text(self, search_terms):
        """

        """


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

    def write_ranked_list(key2value, filename):
        """
        Expects a dict where values are counts
        Writes file (CSV file) of terms, counts, and rank
        """
        values_keys = [(key2value, key) for key in key2value.keys()]
        value_keys.sort(reverse = True)
        with open(filename, 'w') as f:
            csvwriter = csv.writer(f, delimiter='')
            for k,(value,key) in enumerate(value_keys):
                csvwriter.writerow([k,key,value])
