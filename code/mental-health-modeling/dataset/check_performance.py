import csv
from sklearn.metrics import f1_score
from collections import Counter

def uniform(l):
    if l == 1 or l == 2:
       return 1
    return 0

data = [row for row in csv.reader(open("input-interpretations-reddit-test-output.csv"))]
header = data[0]
print(header)
data = data[1:]

preds = []
golds = []
for d_ in data:
    pred = uniform(int(d_[header.index("IP_label")]))
    gold = uniform(int(d_[-1]))
    preds.append(pred)
    golds.append(gold)
print(Counter(preds))
print(f1_score(golds,preds,average="macro"))
