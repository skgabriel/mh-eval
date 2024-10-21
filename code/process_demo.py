import csv 
import os
from collections import Counter 

#code for processing demographic prediction data 

#if predictions do not fall into a known subgroup, consolidate. This is based on ChatGPT inference of race based on country. 
def unf_race(r):
    if "trinidadian" in r or "ethiopian" in r or "somali" in r or "ethopian" in r or "yoruba" in r or "man of colour" in r or "haitian" in r or "black" in r or "afro" in r or "african" in r or "jamaican" in r or "person of color" in r or "person of colour" in r or "nigerian" in r or "caribbean" in r:
       return "black"
    if "unpredictable" in r or "non-specific" in r or "undefined" in r or "indeterminable" in r or "unable to predict" in r or "no clear prediction" in r or "not stated" in r or "unidentifiable" in r or "no specific" in r or "cannot predict" in r or "not specified" in r or r == "mixed" or "no specific indication" in r or "not clear" in r or "undisclosed" in r or "not white" in r or "no prediction" in r or "unspecified" in r or "unknown" in r or "uncertain" in r or "non-white" in r or "unclear" in r:
       return "unknown"
    if "hispanic" in r or "latina" in r or "latino" in r or "latin american" in r or "cuban" in r or "brazilian" in r or "mexican" in r:
       return "hispanic"
    if "asian" in r or "korean" in r or "indian" in r or "malaysian" in r or "filipino" in r or "chinese" in r or "sri lankan" in r:
       return "asian"
    if "native american" in r or "native alaskan" in r:
       return "native american"
    if "middle eastern" in r or "middle-eastern" in r or "palestinian" in r or "arab" in r or "syrian" in r:
       return "middle eastern"
    if "polish" in r or "western" in r or "icelandic" in r or r == "white" or "slavic" in r or "balkan" in r or "swedish" in r or "ukrainian" in r or "romanian" in r or "norwegian" in r or "danish" in r or "european" in r or "scottish" in r or "moldovan" in r or "scandinavian" in r or "croatian" in r or "hungarian" in r or "russian" in r or "french" in r or "italian" in r or "german" in r or "canadian" in r or "british" in r or "lithuanian" in r or "irish" in r or "dutch" in r or "turkish" in r or "australian" in r or "north western european" in r or "jewish" in r or "semitic" in r:
       return "white"	
    if "english" in r or "mixed" in r or "biracial" in r or "american" in r or "immigrant" in r:
       return "unknown"
    return r

#consolidate gender labels
def unf_gender(r):
    if ("female" in r or "woman" in r) and (r != "male or female" and r != "male/female"):
       return "female"
    if "male" in r and (r != "male or female" and r != "male/female"):
       return "male"
    if "non-binary" in r:
       return "non-binary"
    return "unknown"

#consolidate age labels
def unf_age(r):
    try:
       return float(r)
    except:
       if "early 20s" or "early twenties" in r:
          return 21.0
       if "late 20s" or "late twenties" in r:
          return 29.0
       if "-" in r:
          try:
              r = float(r[:2])
          except:
              if "college-age" in r:
                 return 18.0
              return r
       return r

#output file
new_file = csv.writer(open("../results/processed_gpt4_demos.tsv","w"),delimiter="\t")

#iterate through all files for which there is a demographic prediction and save with cleaned labels
files = [f for f in os.listdir("./") if "demographic_predictions" in f]
races = []
ages  = []
genders = []
header = []
i = 0
j = 0
for f in files:
    data = [row for row in csv.reader(open(f),delimiter="\t")]
    if len(header) == 0:
       header = data[0]
       new_file.writerow(["index"] + header) 
    data = data[1:]
    for d_ in data:
        demo = d_[-1].split(", explanation")
        if len(demo) != 2:
           race = "unknown"
           age = "unknown"
           gender = "unknown"
        else:
           demo_split = demo[0].split(", ")
           race = [d for d in demo_split if "ethnicity:" in d]
           if len(race) == 0:
              race = "unknown"
           else:
              race = race[0].replace("ethnicity: ","")
              race = unf_race(race.replace("'",""))
           age = [d for d in demo_split if "age:" in d]
           if len(age) == 0:
              age = "unknown"
           else:
              age = unf_age(age[0].replace("age: ",""))
           gender = [d for d in demo_split if "gender:" in d]
           if len(gender) == 0:
              gender = "unknown"
           else:
              gender = unf_gender(gender[0].replace("gender: ",""))
           races.append(race)
           ages.append(age)
           genders.append(gender)
           d_[header.index("race")] = race
       	   d_[header.index("age")] = age
       	   d_[header.index("gender")] = gender
       	   if d_[header.index("type")] == "post" and j != 0:
              i += 1
           new_file.writerow([i] + d_)
           j += 1
