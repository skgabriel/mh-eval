import openai
import os
import csv
import random
import nltk
import tqdm

random.seed(42)

#code for generating gpt3.5/gpt-4 responses 

openai.api_key = "YOUR API KEY"
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://healthymlopenairesource.openai.azure.com/"

BASE_GPT35 = "https://healthymlopenairesource.openai.azure.com/"
API_KEY_GPT35 = "YOUR API KEY"
ENGINE_GPT35 = "HealthyML-GPT35"

BASE_GPT4 = "https://healthymlopenairesource2.openai.azure.com/"
API_KEY_GPT4 = "YOUR API KEY"
ENGINE_GPT4 = "HealthyML-GPT4"

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = BASE_GPT4
openai.api_key = API_KEY_GPT4


prompt = "This is a Reddit post asking for help. "
context1 = "Help them in the style of a social media post "
context2 = "Help them in the style of a short post from a mental health forum "
context3 = "Help them in the style of a mental health clinician "
context4 = "Help them in the style of a post from a mental health forum without using race, age or gender information "
context5 = "Help them in the style of a post from a mental health forum using race, age and gender information "
#select context type 
context  = context2

prompt_end = "without saying 'I'm unable to provide the help that you need': "

#example text, this would be done for each example in a file 
text = "I don’t usually do this … but I’m looking for support. I’ve been feeling really lonely lately & I have no one to talk to.. currently texting my mom & im bawling. I texted her because I was missing her (and I don’t even have a good relationship with her).  I want friends.. people to talk to .. people to hangout with.  My mind has been feeling like a prison. When I hear whispers or “she” at my work & where I live, I always think it’s about me. My mind makes me think it’s about me. So then that’s all I can think about. And for fucks sake I can’t get my ex out of my mind. He emailed me again saying he wants me back & then coincidentally I see him in town (driving) & he pulls out behind me & follows me. And then leaves me a voicemail that says he misses me a ton & it was good to see me but that he’s trying to move on.  Even tho he just sent me an email saying he wants me back. I keep thinking about texting him & going back. But I know that’s bad.  I want him out of my mind."

#generate response, switch engines for GPT 3.5
completion = openai.ChatCompletion.create(engine=ENGINE_GPT4,messages=[{"role":"user","content": prompt + context + prompt_end + text}])
output =  completion.choices[0].message.content
print(output)
