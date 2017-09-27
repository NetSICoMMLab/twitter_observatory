import network_analyzer
import term_counter
def run(filename):
    tc = term_counter.TermCounter("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    tc.get_ranked_terms()
    tc.tweets_matching_tokens()
    tc.tweets_matching_tokens(self, 20, ["mentions"], True)
    na = network_analyzer.NetworkAnalyzer("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    na.get_edge_list()
    na.get_ranked_in_degree()
