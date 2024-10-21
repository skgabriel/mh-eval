import csv 
import numpy as np
from collections import Counter
from scipy.stats import ttest_ind

context_labels = ["social media","mental health forum","clinician","forum with demographics","forum w/o demographics"]

# read eval file to get results for each metric
def get_data(file):
    data = [row for row in csv.reader(open(file),delimiter="\t")]
    header = data[0]
    data = data[1:]
    #change index depending on prompt type being evaluated
    index = 4
    toxicity = [float(d[-2]) for d in data if (d[-2] != "" and d[-2] != "failed" and d[-1] == context_labels[index])]
    er = [float(d[2]) for d in data if (d[-2] != "" and d[-2] != "failed" and d[-1] == context_labels[index])]
    ip = [float(d[3]) for d in data if (d[-2] != "" and d[-2] != "failed" and d[-1] == context_labels[index])]
    ex  = [float(d[4]) for d in data if (d[-2] != "" and d[-2] != "failed" and d[-1] == context_labels[index])]
    all  = [np.mean([float(d[2]),float(d[3]),float(d[4])]) for d in data if (d[-2] != "" and d[-2] != "failed" and d[-1] == context_labels[index])]
    return toxicity, er, ip, ex, all

output_black = get_data("../mental_llama_responses/eval_set_black_mental_llama_rescored.tsv")
output_asian = get_data("../mental_llama_responses/eval_set_asian_mental_llama_rescored.tsv")
output_white = get_data("../mental_llama_responses/eval_set_white_mental_llama_rescored.tsv")
output_unknown_race = get_data("../mental_llama_responses/eval_set_unknown_race_mental_llama_rescored.tsv")

#change index depending on type of metric used in evaluation
index = 4

print("Black")
print(np.mean(output_black[index]))
print("White")
print(np.mean(output_white[index]))
print("Asian")
print(np.mean(output_asian[index]))
print("Unknown")
print(np.mean(output_unknown_race[index]))
print("Black,White")
print(ttest_ind(output_black[index],output_white[index]))
print("Black,Unknown")
print(ttest_ind(output_black[index],output_unknown_race[index]))
print("Asian,White")
print(ttest_ind(output_asian[index],output_white[index]))
print("Asian, Unknown")
print(ttest_ind(output_asian[index],output_unknown_race[index]))
print("White, Unknown")
print(ttest_ind(output_white[index],output_unknown_race[index]))
