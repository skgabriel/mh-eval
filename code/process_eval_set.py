import json
import numpy as np
import csv
from src.empathy_classifier import EmpathyClassifier
import tqdm
from transformers import pipeline

def toxic_label(output):
    if output["label"] == "LABEL_0":
       return 1-float(output["score"])
    else:
       return float(output["score"])

#assumes use of gpu, otherwise cpu 
device = "cuda"

EX_model_path = "path to trained exploration model" #for example: ./mental-health-modeling/empathy_mental/output_explore/sample2.pth"
ER_model_path = "path to trained emotional reaction model" #for example: "./mental-health-modeling/empathy_mental/output_emotional/sample2.pth"
IP_model_path = "path to trained interpretation model" #for example: "./mental-health-modeling/empathy_mental/output_interpret/sample2.pth"
empathy_classifier = EmpathyClassifier(device, ER_model_path = ER_model_path, IP_model_path = IP_model_path, EX_model_path = EX_model_path,)
sa = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english",return_all_scores=True,device=0,truncation=True,max_length=512)
toxigen_roberta = pipeline("text-classification", model="tomh/toxigen_roberta",truncation=True,max_length=512)

data = json.load(open("../data/eval_sets/eval_set.jsonl"))
black = data["black"]
white = data["white"]
asian = data["asian"]
unknown_race = data["unknown_race"]

missed_care_black = []
missed_care_asian = []
missed_care_white = []
missed_care_unknown = []

levels = ["no","weak","strong"]

#get empathy, toxicity, and sentiment of a given post/reply pair 
def score_reply(text,r_text):
        toxic = toxic_label(toxigen_roberta(r_text)[0])
        (logits_empathy_ER, predictions_ER, logits_empathy_IP, predictions_IP, logits_empathy_EX, predictions_EX, logits_rationale_ER, predictions_rationale_ER, logits_rationale_IP, predictions_rationale_IP, logits_rationale_EX,predictions_rationale_EX) = empathy_classifier.predict_empathy([text], [r_text])
        pred_ER = int(predictions_ER)
        pred_IP = int(predictions_IP)
        pred_EX = int(predictions_EX)
        score = [s["score"] for s in sa(r_text)[0] if s["label"] == "NEGATIVE"][0]
        return [pred_ER, pred_IP, pred_EX, score, toxic]

empathy_black = []

header = ["post","reply","pred_ER","pred_IP","pred_EX","sentiment","toxicity"]

#create new evaluation files

f_black = csv.writer(open("../results/eval_set_black.tsv","w"),delimiter="\t")
f_black.writerow(header)

f_white = csv.writer(open("../results/eval_set_white.tsv","w"),delimiter="\t")
f_white.writerow(header)

f_asian = csv.writer(open("../results/eval_set_asian.tsv","w"),delimiter="\t")
f_asian.writerow(header)

f_unknown_race = csv.writer(open("../results/eval_set_unknown_race.tsv","w"),delimiter="\t")
f_unknown_race.writerow(header)

f_female = csv.writer(open("../results/eval_set_female.tsv","w"),delimiter="\t")
f_female.writerow(header)

f_male  = csv.writer(open("../results/eval_set_male.tsv","w"),delimiter="\t")
f_male.writerow(header)

f_unknown_gender = csv.writer(open("../results/eval_set_unknown_gender.tsv","w"),delimiter="\t")
f_unknown_gender.writerow(header)

f_over_30 = csv.writer(open("../results/eval_set_over_30.tsv","w"),delimiter="\t")
f_over_30.writerow(header)

f_under_30 = csv.writer(open("../results/eval_set_under_30.tsv","w"),delimiter="\t")
f_under_30.writerow(header)

f_unknown_age = csv.writer(open("../results/eval_set_unknown_age.tsv","w"),delimiter="\t")
f_unknown_age.writerow(header)

#process evaluation sets for each subgroup

print("Black Results")
for p in tqdm.tqdm(black.keys()):
    text = p
    if len(black[p]["replies"]) == 0:
       f_black.writerow([text] + [''] * (len(header)-1))
    for reply in black[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_black.writerow([text,r_text] + output )

print("White Results")
for p in tqdm.tqdm(white.keys()):
    text = p
    if len(white[p]["replies"]) == 0:
       f_white.writerow([text] + [''] * (len(header)-1))
    for reply in white[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_white.writerow([text,r_text] + output)

print("Asian Results")
for p in tqdm.tqdm(asian.keys()):
    text = p
    if len(asian[p]["replies"]) == 0:
       f_asian.writerow([text] + [''] * (len(header)-1))
    for reply in asian[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_asian.writerow([text,r_text] + output)

print("Unknown Race Results")
for p in tqdm.tqdm(unknown_race.keys()):
    text = p
    if len(unknown_race[p]["replies"]) == 0:
       f_unknown_race.writerow([text] + [''] * (len(header)-1))
    for reply in unknown_race[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_unknown_race.writerow([text,r_text] + output)

print("Female Results")
for p in tqdm.tqdm(female.keys()):
    text = p
    if len(female[p]["replies"]) == 0:
       f_female.writerow([text] + [''] * (len(header)-1))
    for reply in female[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_female.writerow([text,r_text] + output)

print("Male Results")
for p in tqdm.tqdm(male.keys()):
    text = p
    if len(male[p]["replies"]) == 0:
       f_male.writerow([text] + [''] * (len(header)-1))
    for reply in male[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_male.writerow([text,r_text] + output)

print("Unknown Gender Results")
for p in tqdm.tqdm(unknown_gender.keys()):
    text = p
    if len(unknown_gender[p]["replies"]) == 0:
       f_unknown_gender.writerow([text] + [''] * (len(header)-1))
    for reply in unknown_gender[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_unknown_gender.writerow([text,r_text] + output)

print("Over 30 Results")
for p in tqdm.tqdm(over_30.keys()):
    text = p
    if len(over_30[p]["replies"]) == 0:
       f_over_30.writerow([text] + [''] * (len(header)-1))
    for reply in over_30[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_over_30.writerow([text,r_text] + output)

print("Under 30 Results")
for p in tqdm.tqdm(under_30.keys()):
    text = p
    if len(under_30[p]["replies"]) == 0:
       f_under_30.writerow([text] + [''] * (len(header)-1))
    for reply in under_30[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
        f_under_30.writerow([text,r_text] + output)

print("Unknown Age Results")
for p in tqdm.tqdm(unknown_age.keys()):
    text = p
    if len(unknown_age[p]["replies"]) == 0:
       f_unknown_age.writerow([text] + [''] * (len(header)-1))
    for reply in unknown_age[p]["replies"]:
        r_text = reply[0]
        output = score_reply(text,r_text)
