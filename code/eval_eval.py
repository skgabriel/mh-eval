import csv 
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind

#evaluate human responses from peer-to-peer data

def get_data(file):
    data = [row for row in csv.reader(open(file),delimiter="\t")]
    header = data[0]
    data = data[1:]
    posts = [d[0] for d in data]
    #get num replies
    replies = [d[1] for d in data]
    already = []
    all_replies = Counter([d[0] for d in data])
    for d in data:
        if d[0] in already:
           continue
        else:
           already.append(d[0])
           if d[-1] == "":
              replies.append(0)
           else:
              replies.append(all_replies[d[0]])
    sentiment = [float(d[-2]) for d in data if d[-2] != ""]
    toxicity = [float(d[-1]) for d in data if d[-1] != ""]
    er = [float(d[2]) for d in data if d[2] != ""]
    ip = [float(d[3]) for d in data if  d[3] != ""]
    ex  = [float(d[4]) for d in data if d[4] != ""]
    all  = [np.mean([float(d[2]),float(d[3]),float(d[4])]) for d in data if d[2] != ""]
    return sentiment, toxicity, er, ip, ex, all, posts, replies

output_black = get_data("../data/eval_sets/eval_set_black.tsv")
output_asian = get_data("../data/eval_sets/eval_set_asian.tsv")
output_white = get_data("../data/eval_sets/eval_set_white.tsv")
output_unknown_race = get_data("../data/eval_sets/eval_set_unknown_race.tsv")

print("asian")
print(np.mean(output_asian[4]))
print("black")
print(np.mean(output_black[4]))
print("white")
print(np.mean(output_white[4]))
print("unknown")
print(np.mean(output_unknown_race[4]))
print("black/white")
print(ttest_ind(output_black[4],output_white[4]))
print("black/unknown")
print(ttest_ind(output_black[4],output_unknown_race[4]))
print("asian/white")

print(ttest_ind(output_asian[4],output_white[4]))
print("asian/unknown")
print(ttest_ind(output_asian[4],output_unknown_race[4]))
print("white/unknown")
print(ttest_ind(output_white[4],output_unknown_race[4]))
