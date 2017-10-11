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
import term_counter
from ttp import ttp
#import networkx as nx
from collections import Counter

class NetworkAnalyzer:
    """
    Builds networks for returning network statistics and data

    Example:
        import network_analyzer
        network_analyzer.NetworkAnalyzer(parameters............)

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

    n_nodes, int

    n_edges, int

    edge2weight, dict (source/target tuple -> weight)
    """

    def __init__(self, tweet_dir, working_dir=None):
        self.tweet_dir = tweet_dir
        self.n_nodes = 0
        self.n_edges = 0
        self.edge2weight = Counter()
        self.node2in_deg = Counter()
        if working_dir is None:
            self.working_dir = os.getcwd()
        else:
            self.working_dir = working_dir
        if 'reduced' in self.tweet_dir:
            self.reduced_data = True
        else:
            self.reduced_data = False

    def get_edge_list(self):
        # List out tweet files
        tweet_files = os.listdir(self.tweet_dir)
        # Get edges from each tweet file
        for filename in tweet_files:
            print filename
            file_edges = self.get_edges_from_file(filename)
            self.edge2weight.update(file_edges)
        # Get size of network (nodes and edges)
        self.get_network_size()
        # Output the edge list
        output_dir = self.working_dir+'/network_stats'
        try:
            os.makedirs(output_dir)
        except:
            print "File '"+output_dir+"' exists"
        self.write_edge_list(self.edge2weight, output_dir+'/edge-list.csv')

    def graph_from_edge_list(self):
        output_dir = self.working_dir+'/network_stats'
        G=nx.read_weighted_edgelist(output_dir+'/edge-list.csv')
        graphs = list(nx.connected_component_subgraphs(G))
        lcc = sorted(graphs, key=lambda graph: len(graph.nodes()), reverse=True)[0]
        try:
            diameter = nx.diameter(G)
        except:
            diameter = "NA"
        return {'node_count': len(G.nodes()), 'edge_count': len(G.edges()), 'component_count': len(graphs), 'lcc_node_count': len(lcc.nodes()), 'lcc_edge_count': len(lcc.edges()), 'diameter': diameter, 'lcc_diameter': nx.diameter(lcc)}

    def get_edges_from_file(self, filename):
        edge2weight = Counter()
        with open(self.tweet_dir+'/'+filename, 'rb') as f:
            # Open the file differently based on CSV or JSON
            if self.reduced_data is True:
                tweet_file = self.a_most_dirty_hand(csv.reader(f, delimiter='\t'))
            else:
                tweet_file = f
            # Read through each line of the file and update Counters
            null_rows = 0
            for tweet in tweet_file:
                # try:
                if self.reduced_data is True:
                    user = tweet[-1]
                    text = unicode(tweet[9], 'utf-8')
                else:
                    tweet = json.loads(line)
                    user = 5#TODO: fill in
                    text = unicode(tweet['text'], 'utf-8')
                mentions = term_counter.TermCounter("", "").mentions(text)
                # Make edges of user with all mentions
                for mention in mentions:
                    edge2weight.update([(user, mention)])
                # except:
                #     print "Null row."
                #     null_rows += 1
        return edge2weight

    def get_network_size(self):
        if len(self.edge2weight.keys()) == 0:
            print 'Need an edge list to get network size'
            return

        self.n_edges = len(self.edge2weight.keys())
        nodes = set()
        for edge in self.edge2weight.keys():
            nodes.update(edge)
        self.n_nodes = len(nodes)

    def get_ranked_in_degree(self):
        if len(self.edge2weight.keys()) == 0:
            print 'Need an edge list to get the ranked in-degrees'
            sys.exit()

        # Get in-degree for each node
        for edge in self.edge2weight:
            self.node2in_deg.update([edge[1]])
        # Output the ranked list by in-degree
        output_dir = self.working_dir+'/network_stats'
        try:
            os.makedirs(output_dir)
        except:
            print "File '"+output_dir+"' exists"
        self.write_ranked_list(self.node2in_deg, output_dir+'/ranked-indegree.csv')


    # --------------------------------------------------------------------------
    # ---------------------------- Helper functions ----------------------------
    # --------------------------------------------------------------------------
    def write_ranked_list(self, key2value, filename):
        """
        Expects a dict where values are counts
        Writes file (CSV file) of terms, counts, and rank
        """
        # Dict -> sorted list of (value, key) pairs in high->low order
        values_keys = [(key2value[key], key) for key in key2value]
        values_keys.sort(reverse = True)
        # Write ranks, keys, and values, to file
        with open(filename, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for k,(value,key) in enumerate(values_keys):
                csvwriter.writerow([k,key,value])

    def write_edge_list(self, edge2weight, filename):
        """
        Expects a dict where values are weights of tuple edges
        Writes file (CSV file) of source, target, weight
        """
        # Dict -> sorted list of (value, key) pairs in high->low order
        weight_edges = [(edge2weight[edge], edge) for edge in edge2weight]
        weight_edges.sort(reverse = True)
        # Write ranks, keys, and values, to file
        with open(filename, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for (weight,edge) in weight_edges:
                csvwriter.writerow([edge[0],edge[1],weight])

    def a_most_dirty_hand(self, csv_reader):
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                # error handling what you want.
                pass
            continue
        return
