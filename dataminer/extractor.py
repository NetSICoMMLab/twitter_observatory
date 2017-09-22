"""CoMM Lab Tweet Extractor (extractor.py)
Extracts tweets from the Gardenhose (either from the full JSON files or
summarized CSV files) based on a keyword or set of keywords and outputs matched
tweets for later analysis. User can search for several keywords/hashtags
individually or search for tweets containing *all* of the specified keywords.

Contributors:
Devin Gaffney & Ryan J. Gallagher
Network Science Institute, Northeastern University, 2017
"""
import os
import csv
import json
from datetime import datetime

class Extractor:
    """
    Extracts tweets from the Gardenhose

    Example:
        import extractor
        extractor.Extractor(['#BlackLivesMatter', '#Ferguson'], 'OR', '2014-08-09',
                            '2015-08-09', 'reduced', 'blm_hashtags')

    Parameters
    ----------
    hashtag_set: list (iterable?) of strings (hashtag->keyword)
        Keywords to search for in Gardenhose tweets

    hashtag_operator: string, "AND" or "OR"
        Specifies type of keyword search. "AND" queries search for tweets
        where all keywords appear. "OR" queries search individually for each
        keyword in tweets

    start_time: string, "YYYY-MM-DD" (extend possibility for to the hour?)
        Start date of the search

    end_time: string, "YYYY-MM-DD"
        End date of the search

    data_fullness: string, "reduced" or "full"
        Specifies which tweet files to search. "reduced" queries search the
        summarized CSV files, which are faster to search but only have the
        most commonly used fields (limiting downstream analysis). "full" queries
        search the raw JSON files, which have all the tweet fields, but are much
        slower to search through

    corpus_dir: string
        Directory off the working directory in which to put the extracted tweets

    working_directory: string
        Working directory in which to make folder containing matched tweets

    Attributes
    ----------
    full_data_path: string
        File path to raw JSON files

    reduced_data_path: string
        File path to summarized CSV files

    current_user: string
        Username of the current user on the Achtung servers

    start_datetime: datetime
        Datetime object of start date string

    end_datetime: datetime
        Datetime object of end date string
    """
    def __init__(self,hashtag_set, hashtag_operator='OR', start_time='2011-07-01',
                 end_time='2016-12-01', data_fullness='reduced',
                 corpus_dir='hashtag_extractions', working_directory=None):
        # TODO: more integrity checks of passed paramters
        # Initialize parameters of search
        self.hashtag_set = hashtag_set
        self.start_time = start_time
        self.end_time = end_time
        self.data_fullness = data_fullness
        self.hashtag_operator = hashtag_operator
        self.current_user = os.popen('whoami').read().split('\n')[0]
        self.full_data_path = '/net/twitter/gardenhose-data/json'
        self.reduced_data_path = '/net/twitter/gardenhose-data/summarized'
        if working_directory == None:
            self.working_directory="/home/"+self.current_user()
        # Validate start and end date
        try:
            self.start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
            self.end_datetime = datetime.strptime(end_time, '%Y-%m-%d')
        except ValueError:
            date_string = 'Start date = {}, End date = {}'.format(start_date, end_date)
            print('Invalid time range, cannot parse time:\n' + date_string)
            sys.exit()
        if (end_time-start_time).days < 0:
            date_string = 'Start date = {}, End date = {}'.format(start_date, end_date)
            print('Invalid time range, end date before start date:\n' + date_string))
            sys.exit()

        # Extract tweets based on hashtag operator
        if hashtag_operator == "AND":
            print "Extracting "+str.join(",", hashtag_set)
            self.extract(hashtag_set)
        elif hashtag_operator == "OR":
            for hashtag in hashtag_set:
                print "Extracting "+hashtag
            self.extract([hashtag])
        else:
            return "Hashtag Operator MUST BE AND or OR, you goof."

    def extract(self, search_hashtags):
        """
        Directs collection of files according to the data fullness parameter and
        then extracts matched tweets from files

        INPUT
        -----
        search_hashtags: list (iterable?)
            Either an array of length one (in the case we are doing an "OR"
            search) or an array of several hashtags (in the case we are doing an
            "AND" search)
        """
        # Get the relevant files depending on data fullness
        if data_fullness == 'reduced':
            files = self.restricted_to_timeline(self.ls(self.reduced_data_path))
        else:
            files = self.restricted_to_timeline(self.ls(self.full_data_path))
        # Make directory to place tweets
        #TODO: also write a flat file at this point specifying what is being requested/when/who requested it
        full_corpus_path = self.make_corpus_dir(search_hashtags)
        # Search tweets in each file for matches
        for file in files:
            self.extract_file(file, search_hashtags, full_corpus_path)

    def extract_file(self, file, search_hashtags, full_corpus_path):
        """
        Searches a single file for matches to the given hashtags

        INPUT
        -----
        file, string
            File to search through for matches to hashtags
        search_hashtags, list
            As in extract()
        full_corpus_path, string
            Full file path to the directory where matched tweet files are placed
        """
        #TODO: awk does not capture totally unique hashtags but instead captures substrings of hashtags - eg. searching for #ff will also extract #ffvi #ffix and etc
        print "\t"+file
        if self.data_fullness == 'reduced':
            os.popen("lz4 -dc "+self.reduced_data_path+"/"+file+" | awk '/"+str.join("/ && /", search_hashtags)+"/' > "+full_corpus_path+str.replace(file, ".lz4", ".csv"))
        elif self.data_fullness == 'full':
            os.popen("xzcat "+self.full_data_path+"/"+file+" | awk '/"+str.join("/ && /", search_hashtags)+"/' > "+full_corpus_path+str.replace(file, ".xz", ".csv"))


    # ---------------------------- Helper functions ----------------------------
    def make_corpus_dir(self, search_hashtags):
        """
        Makes the directory for files of matched tweets

        OUTPUT
        ------
        full_corpus_path, string
            Path to the directory where matched tweet files are placed
        """
        # Concatenate hashtags into a string
        hashtag_str = str.join('-',search_hashtags)
        # Construct name of directory where to place tweets
        corpus_name = hashtag_str+'-'+self.start_time+'-'+self.end_time+'-'+self.data_fullness
        # Construct the path to the directory where tweets will be placed
        full_corpus_path = working_directory+'/'+self.corpus_dir'/'+corpus_name
        # Make the directory
        os.mkdirs(full_corpus_path)
        return full_corpus_path

    def restricted_to_timeline(self, files):
        """
        Takes a list of files from the Achtung server and determines if they
        fall within the specified date range

        OUTPUT
        ------
        ranged_files, list
            List of files that fall within the specified date range
        """
        ranged_files = []
        for file in files:
            if ".lz4" in file or ".xz" in file:
                file_time = datetime.strptime(file.split(".")[-2], '%Y-%m-%d')
            if self.start_datetime <= file_time and file_time <= self.end_datetime:
                ranged_files.append(file)
        return ranged_files

    def ls(self, path):
        """
        Returns a sorted list of files in a directory
        """
        return sorted(os.listdir(path))
