import csv
import json

#group posts by GPT-4 predicted subgroup 

data = [row for row in csv.reader(open("../data/processed_gpt4_demos.tsv"),delimiter="\t")]
header = data[0]
data = data[1:]

black_r =  []
asian_r =  []
white_r  = []
unknown_r = []

female_g = []
male_g = []
unknown_gender = []

under_30 = []
over_30 = []
unknown_age = []

#restore all replies (missing from gpt-4 prediction file which is all posts)
replies = json.load(open("../data/replies.jsonl"))
eval_set = {"black":{},"white":{},"asian":{},"unknown_race":{},"female":{},"male":{},"unknown_gender":{},"over_30":{},"under_30":{},"unknown_age":{}}
eval_file = open("eval_set.jsonl","w")

#add each post to a dict for creating the eval set json file based on subgroup
for i,d_ in enumerate(data):
    try:
        r = replies[d_[header.index("text")]]["replies"]   
    except:
        continue 
    if d_[header.index("race")] == "black" and d_[header.index("type")] == "post":
       black_r.append(i)  
       eval_set["black"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"gender":d_[header.index("gender")]}
    if d_[header.index("race")] == "white" and d_[header.index("type")] == "post":
       white_r.append(i)
       eval_set["white"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"gender":d_[header.index("gender")]}
    if d_[header.index("race")] == "asian" and d_[header.index("type")] == "post":
       asian_r.append(i)
       eval_set["asian"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"gender":d_[header.index("gender")]}
    if d_[header.index("race")] == "unknown" and d_[header.index("type")] == "post":
       unknown_r.append(i)
       eval_set["unknown_race"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"gender":d_[header.index("gender")]}

    if d_[header.index("gender")] == "female" and d_[header.index("type")] == "post":
       female_g.append(i)
       eval_set["female"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"race":d_[header.index("race")]}
    if d_[header.index("gender")] == "male" and d_[header.index("type")] == "post":
       male_g.append(i)
       eval_set["male"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"race":d_[header.index("race")]}
    if d_[header.index("gender")] == "unknown" and d_[header.index("type")] == "post":
       unknown_gender.append(i)
       eval_set["unknown_gender"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"age":d_[header.index("age")],"race":d_[header.index("race")]}

    if d_[header.index("age")] != "unknown" and float(d_[header.index("age")]) >= 30 and d_[header.index("type")] == "post":
       over_30.append(i)
       eval_set["over_30"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"race":d_[header.index("race")],"gender":d_[header.index("gender")]}
    if d_[header.index("age")] != "unknown" and float(d_[header.index("age")]) < 30 and d_[header.index("type")] == "post":
       under_30.append(i)
       eval_set["under_30"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"race":d_[header.index("race")],"gender":d_[header.index("gender")]}
    if d_[header.index("age")] == "unknown" and d_[header.index("type")] == "post":
       unknown_age.append(i)
       eval_set["unknown_age"][d_[header.index("text")]] = {"author":d_[header.index("author")],"replies":r,"race":d_[header.index("race")],"gender":d_[header.index("gender")]}
json.dump(eval_set,eval_file)

#Dataset sets
print("Race")
print(len(black_r))
print(len(white_r))
print(len(unknown_r))
print(len(asian_r))
print("")

print("Gender")
print(len(female_g))
print(len(male_g))
print(len(unknown_gender))
print("")

print("Age")
print(len(under_30))
print(len(over_30))
print(len(unknown_age))
print("")
