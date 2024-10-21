import csv
import numpy as np

#get appropriate numeric answer based on expert response to question
def rescore(type,response):
    if type == "er":
       if response == "No":
          return 0
       elif "feelings are not explicitly" in response:
          return 1
       else:
          return 2
    elif type == "ip":
       if response == "No":
          return 0 
       elif "a shallow understanding" in response:
          return 1
       else:
          return 2 
    elif type == "ex":
       if response == "No":
          return 0
       elif "is generic" in response:
          return 1
       else:
          return 2 
    else:
       return int(response.split(":")[0])

#data from expert evaluation
data = [row for row in csv.reader(open("../data/expert_eval/expert_eval_most_recent.csv"))]
#original file of examples shown to experts 
data2 = [row for row in csv.reader(open("../data/expert_eval/expert_evaluation2.csv"))]
header2 = data2[0]
data2 = data2[1:]
header = data[0]
data_1 = data[3]
data_2 = data[4]

i = 0
# store results from experts 
q_dict1 = {"er":[],"ip":[],"ex":[],"ct":[],"st":[],"pa":[]}
q_dict2 = {"er":[],"ip":[],"ex":[],"ct":[],"st":[],"pa":[]}

# all question types, includes answers to partnership and sustain talk questions not considered in this study 
q_types = ["er","ip","ex","ct","st","pa"]

#parse results from raw qualtrics data 
for q in header:
    #skip non-question fields and final manipulation check (q14)
    if "Q" not in q or q == "Q14_1":
       continue
    #reset to match index i to a question type 
    if i > 5:
       i = 0  
    response1 = data_1[header.index(q)] #response for expert 1
    response2 = data_2[header.index(q)] #response for expert 2 
    q_dict1[q_types[i]].append(rescore(q_types[i],response1)) # get question answer based on type 
    q_dict2[q_types[i]].append(rescore(q_types[i],response2)) # get question answer based on type 
    i += 1

#For following results, switch between q_dict1 and q_dict2 (or data_1 and data_2) for experts 1 and 2 

print("Emotional Reaction")
print(np.mean([q_dict1["er"][i] for i in range(len(q_dict1["er"])) if "human" in data2[i][-2].lower()]))
print(np.mean([q_dict1["er"][i] for i in range(len(q_dict1["er"])) if "ai" in data2[i][-2].lower()]))

print("Interpretation")
print(np.mean([q_dict1["ip"][i] for i in range(len(q_dict1["er"])) if "human" in data2[i][-2].lower()]))
print(np.mean([q_dict1["ip"][i] for i in range(len(q_dict1["er"])) if "ai" in data2[i][-2].lower()]))

print("Exploration")
print(np.mean([q_dict1["ex"][i] for i in range(len(q_dict1["er"])) if "human" in data2[i][-2].lower()]))
print(np.mean([q_dict1["ex"][i] for i in range(len(q_dict1["er"])) if "ai" in data2[i][-2].lower()]))

print("Change Talk")  
print(np.mean([q_dict1["ct"][i] for i in range(len(q_dict1["er"])) if "human" in data2[i][-2].lower() and q_dict2["ct"][i] != 6]))
print(np.mean([q_dict1["ct"][i] for i in range(len(q_dict1["er"])) if "ai" in data2[i][-2].lower() and q_dict2["ct"][i] != 6]))

print("% AI")
print(data_1[header.index("Q14_1")])
#actual percentage of ai examples 
print(np.mean([ "ai" in data2[i][-2].lower() for i in range(50)]))
