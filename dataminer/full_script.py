import network_analyzer
import term_counter
import time_analyzer
filename = "#AltonSterling_2015-08-09_2017-08-09_reduced"
def run(filename):
    tc = term_counter.TermCounter("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    tc.get_ranked_terms()
    tc.tweets_matching_tokens()
    tc.tweets_matching_tokens(20, ["mentions"], True)
    tc.get_counts()
    na = network_analyzer.NetworkAnalyzer("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    na.get_edge_list()
    na.graph_from_edge_list()
    na.get_ranked_in_degree()

def run_short(filename):
    tc = term_counter.TermCounter("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    print tc.get_counts()
    na = network_analyzer.NetworkAnalyzer("/home/dgaffney/hashtag_extractions/"+filename, "/home/dgaffney/hashtag_results/"+filename)
    print na.basic_stats()


filename = "#AllMenCan_2014-02-01_2016-02-01_reduced"
filename = "#AltonSterling_2015-08-09_2017-08-09_reduced"
filename = "#Baltimore_2015-08-09_2017-08-09_reduced"
filename = "#BaltimoreRiots_2015-08-09_2017-08-09_reduced"
filename = "#BaltimoreUprising_2015-08-09_2017-08-09_reduced"
filename = "#BlackLivesMatter_2015-08-09_2017-08-09_reduced"
filename = "#CrimingWhileWhite_2014-02-01_2016-02-01_reduced"
filename = "#EricGarner_2015-08-09_2017-08-09_reduced"
filename = "#FastTailedGirls_2014-02-01_2016-02-01_reduced"
filename = "#FemFuture_2014-02-01_2016-02-01_reduced"
filename = "#Ferguson_2015-08-09_2017-08-09_reduced"
filename = "#FreddieGray_2015-08-09_2017-08-09_reduced"
filename = "#ICantBreathe_2015-08-09_2017-08-09_reduced"
filename = "#PhilandoCastile_2015-08-09_2017-08-09_reduced"
filename = "#SandraBland_2015-08-09_2017-08-09_reduced"
filename = "#SayHerName_2015-08-09_2017-08-09_reduced"
filename = "#SurvivorPrivilege_2014-02-01_2016-02-01_reduced"
filename = "#TamirRice_2015-08-09_2017-08-09_reduced"
filename = "#TheEmptyChair_2014-02-01_2016-02-01_reduced"
filename = "#WalterScott_2015-08-09_2017-08-09_reduced"
filename = "#WhyIStayed_2014-02-01_2016-02-01_reduced"
filename = "#YesAllWomen_2014-02-01_2016-02-01_reduced"
filename = "#YouOKSis_2014-02-01_2016-02-01_reduced"

import time_analyzer
ta = time_analyzer.TimeAnalyzer("/home/dgaffney/hashtag_extractions/#YouOKSis_2014-02-01_2016-02-01_reduced", "/home/dgaffney/hashtag_results/#YouOKSis_2014-02-01_2016-02-01_reduced")
timeline = ta.write_timelines()
sorted(timeline.keys())