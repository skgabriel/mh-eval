
### Guide to Data Directory ###

all_scraped_data: Posts, responses and metadata from Reddit scraping before LLM generation 

processed.tsv contains all scraped data with the following fields:

- text: text of Reddit post or reply
- author: author of original Reddit post 
- type: post or reply
- age: predicted age of the poster (na for replies) 
- gender: predicted gender of the poster (na for replies)
- race: predicted race of the poster (na for replies)
- sentiment: predicted sentiment of the text 
- empathy_er: predicted emotional reaction empathy (no, weak, strong; na for posts)
- empathy_ip:  predicted interpretation empathy (no, weak, strong; na for posts)
- empathy_ex:  predicted exploration empathy (no, weak, strong; na for posts)
- num_replies: number of replies to a post (na for replies) 
- community: the Reddit community a post or reply comes from

counterfactuals: data from counterfactual experiments with original Reddit posts deemed to be "neutral," modified posts, and LLM generations 

For files ending in *_gpt4.tsv, there are two subfields with the post and a GPT-4 response. Otherwise, the file only contains a post. 

eval_sets: eval splits for demographic subgroups before LLM generation 

There are 10 eval sets for race, age and gender:

- eval_set_asian.tsv
- eval_set_black.tsv
- eval_set_white.tsv
- eval_set_unknown_race.tsv

- eval_set_female.tsv
- eval_set_male.tsv
- eval_set_unknown_gender.tsv

- eval_set_over_30.tsv
- eval_set_under_30.tsv
- eval_set_unknown_age.tsv

For each, every post/reply pair is a separate row. There are the following fields:

- post: the text of the post (there can be multiple rows with the same post text) 
- reply: the text of the reply (from a human peer-to-peer responder)  
- pred_ER: predicted emotional reaction empathy of the reply 
- pred_IP: predicted interpretation empathy of the reply 
- pred_EX: predicted exploration empathy of the reply 
- sentiment: predicted sentiment of the reply 
- toxicity: predicted toxicity of the reply 

gpt3.5_responses: GPT-3.5 generations for race subgroup eval sets 

Each file has the following fields:

- post: the text of the post
- reply: the text of the GPT3.5 response 
- pred_ER: predicted emotional reaction	empathy	of the reply 
- pred_IP: predicted interpretation empathy of the reply 
- pred_EX: predicted exploration empathy of the	reply 
- sentiment: predicted sentiment of the reply 
- toxicity: predicted toxicity of the reply
- type: prompt type used for generating the response (e.g. clinician)

Note that there may be a mismatch in size for some eval sets with LLM generations and the original eval sets. This is due to a small number of examples being rejected by the API. 

gpt4_responses: GPT-4 generations for all eval sets

Each file has the following fields:

- post: the text of the post
- reply: the text of the GPT3.5 response
- pred_ER: predicted emotional reaction empathy of the reply
- pred_IP: predicted interpretation empathy of the reply
- pred_EX: predicted exploration empathy of the reply
- sentiment: predicted sentiment of the reply
- toxicity: predicted toxicity of the reply
- type:	prompt type used for generating the response (e.g. clinician)

Note that there may be a mismatch in size for some eval sets with LLM generations and the original eval sets. This is due to a small number of examples being rejected by the API.

mental_llama_responses: Mental-Llama generations for eval sets

- post: the text of the post
- reply: the text of the GPT3.5 response
- pred_ER: predicted emotional reaction empathy of the reply
- pred_IP: predicted interpretation empathy of the reply
- pred_EX: predicted exploration empathy of the reply
- sentiment: predicted sentiment of the reply
- toxicity: predicted toxicity of the reply
- type: prompt type used for generating the response (e.g. clinician)

expert_eval: raw data from clinician evaluation on Qualtrics 

expert_eval_most_recent.csv contains two different rows for expert 1 and expert 2 evaluations 

expert_evaluation2.csv contains the examples shown to clinicians with labels for AI or human response

processed_gpt4_demos.tsv: file with GPT-4 demographic inference information for Reddit posts (used to create subgroup splits) 

original_demo_pred: individual files with demographic predictions from GPT-4 for each subreddit

original_reddit: individual files for each subreddit

replies.jsonl: all replies extracted from post data
