import openai
import csv
import spacy_fastlang
import spacy
import tqdm

#GPT-4 race, gender and age prediction 

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('language_detector')


#specify your api key 
openai.api_key = "[YOUR API Key]"
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://healthymlopenairesource.openai.azure.com/"

BASE_GPT35 = "https://healthymlopenairesource.openai.azure.com/"
API_KEY_GPT35 = "[YOUR API Key]"
ENGINE_GPT35 = "HealthyML-GPT35"

BASE_GPT4 = "https://healthymlopenairesource2.openai.azure.com/"
API_KEY_GPT4 = "[YOUR API Key]"
ENGINE_GPT4 = "HealthyML-GPT4"

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = BASE_GPT4
openai.api_key = API_KEY_GPT4

#set a specific reddit post file to predict for, this uses the example of "processed_anxiety.tsv"
data = [row for row in csv.reader(open("../data/reddit_data/processed_anxiety.tsv"),delimiter="\t")]
header = data[0]
data = data[1:]

prompt_start = "Predict the ethnicity, age and gender of the author who wrote this post: "
prompt_end = ". The answer should be formatted like this 'ethnicity: asian, age: 18, gender: female, explanation: she self-identifies as a teenage asian woman.','ethnicity: black, age: 40s, gender: female, explanation: Considering the mention of ‘knotless braids’, a style popularly associated with Black culture, and the underlying humor about growing them out all her life, it is not arguable that the author is Black. The mention of ‘my bf’ and the nature of the interaction also suggests that the author is female.' If you cannot predict, answer with 'no prediction.'"

#output file name
results = csv.writer(open("../results/demographic_predictions_anxiety.tsv","w"),delimiter="\t")
results.writerow(header + ["demo_prediction"])

#for each post in file, make a prediction. skip posts that are very short or not in english. 
for d_ in tqdm.tqdm(data):
    text = d_[0]
    doc = nlp(text)
    detect_language = doc._.language
    if len(text.split(" ")) < 10 or detect_language != "en":
       continue
    try:
        completion = openai.ChatCompletion.create(engine=ENGINE_GPT4,messages=[{"role":"user","content": prompt_start + text + prompt_end}])
        completion = completion.choices[0].message.content
    except:
        completion = "failed"
    results.writerow(d_ + [completion.lower()])    
    if "no prediction" not in completion.lower():
        print(completion)
