import term_counter
tc = term_counter.TermCounter("/home/dgaffney/hashtag_extractions/#AltonSterling_2015-08-09_2017-08-09_reduced", "/home/dgaffney/hashtag_results/#AltonSterling_2015-08-09_2017-08-09_reduced")
tc.get_ranked_terms()
tc.tweets_matching_tokens()
tc.tweets_matching_tokens(self, 20, ["mentions"], True)
import network_analyzer
na = network_analyzer.NetworkAnalyzer("/home/dgaffney/hashtag_extractions/#AltonSterling_2015-08-09_2017-08-09_reduced", "/home/dgaffney/hashtag_results/#AltonSterling_2015-08-09_2017-08-09_reduced")
