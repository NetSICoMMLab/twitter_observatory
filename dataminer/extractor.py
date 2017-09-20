#- Extract Hashtags within a time-frame (extractor.py)
#  - OR and AND support for multiple hashtags (extractor.py)
#  - Extracted Content is placed into a unified corpus layout (extractor.py)
import csv
import json
import os
from datetime import datetime
class Extractor:
  def current_user():
    return os.popen("whoami").read().split("\n")[0]
  
  def kickoff(hashtag_set, hashtag_operator, start_time, end_time, data_fullness=None, working_directory=None):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    if end_time-start_time < 0:
      return "I can't go backwards in time!"
    if data_fullness == None:
      data_fullness="reduced"
    if working_directory == None:
      working_directory="/home/"+current_user()
    if hashtag_operator == "AND":
    elif hashtag_operator == "OR":
        print "Extracting "+str.join(",", hashtag_set)
        extract(hashtag_set, start_time, end_time, data_fullness, working_directory)
      for hashtag in hashtag_set:
        print "Extracting "+hashtag
        extract([hashtag], start_time, end_time, data_fullness, working_directory)
    else:
      return "Hashtag Operator MUST BE AND or OR, you goof."
  
  def extract(hashtag_set, start_time, end_time, data_fullness, working_directory):
    files = []
    if data_fullness == "reduced":
      files = restricted_to_timeline(ls(reduced_data_path()), start_time, end_time)
    else:
      files = restricted_to_timeline(ls(full_data_path()), start_time, end_time)
    create_corpus(hashtag_set, start_time, end_time, data_fullness, working_directory)
    for file in files:
      extract_file(file, hashtag_set, data_fullness)
  
  def fullpath(working_directory, hashtag_set, start_time, end_time, data_fullness):
    return working_directory+"/hashtag_extractions/"+corpus_name(hashtag_set, start_time, end_time, data_fullness)+"/"

  def extract_file(file, working_directory, hashtag_set, data_fullness, working_directory):
    if data_fullness == "reduced":
      os.popen("lz4 -dc "+reduced_data_path()+"/"+file+" | awk '/"+str.join("/ && /", hashtag_set)+"/' > "+fullpath(working_directory, hashtag_set, start_time, end_time, data_fullness)+str.replace(file, ".lz4", ".csv"))
      #todo awk does not capture totally unique hashtags but instead captures substrings of hashtags - eg. searching for #ff will also extract #ffvi #ffix and etc
    else:
      os.popen("xzcat "+full_data_path()+"/"+file+" | awk '/"+str.join("/ && /", hashtag_set)+"/' > "+fullpath(working_directory, hashtag_set, start_time, end_time, data_fullness)+str.replace(file, ".xz", ".csv"))
  
  def corpus_name(hashtag_set, start_time, end_time, data_fullness):
    return str.join("_", hashtag_set)+"_"+start_time.strftime("%Y-%m-%d")+"_"+end_time.strftime("%Y-%m-%d")+"_"+data_fullness
  
  def create_corpus(hashtag_set, start_time, end_time, data_fullness):
    os.popen("mkdir -p "+working_directory+"/hashtag_extractions/"+corpus_name(hashtag_set, start_time, end_time, data_fullness))
    #todo also write a flat file at this point specifying wtf it is that we've requested off the servers.
  
  def restricted_to_timeline(files, start_time, end_time):
    ranged_files = []
    for file in files:
      this_time = datetime.strptime(file.split(".")[-1], '%Y-%m-%d')
      if start_time <= this_time and this_time <= end_time:
        ranged_files.append(file)
    return ranged_files
    
  def full_data_path():
    return "/net/twitter/gardenhose-data/json"
  
  def reduced_data_path():
    return "/net/twitter/gardenhose-data/summarized"
    
  def ls(path):
    return sorted(os.listdir(path))
