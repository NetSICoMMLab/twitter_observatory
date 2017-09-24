"""Network Analyzer (network_analyzer.py)
Takes a directory of tweets, builds a network, and returns relevant statistics
about the network

Contributors:
Devin Gaffney & Ryan J. Gallagher
Network Science Institute, Northeastern University, 2017
"""
import os
import csv
import json
import networkx as nx

class Network_Analyzer:
    """
    Builds networks for returning network statistics and data

    Example:
        import network_analyzer
        network_analyzer.Network_Analyzer(parameters............)

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
