import praw
import json
import tqdm

#check if name of author was properly fetched 
def check_valid(name):
    if name != None:
       return name.name
    return "" 

#list of subreddits for scraping 
all_subr = ["EatingDisorders"]

#set up 
reddit = praw.Reddit(
    client_id="KVyT4zabo7Q6mLCFyH7FzA",
    client_secret="ODTt1hKwpMSpon-Dxapj-st7ZQtIeQ",
    user_agent="my user agent",
)

#for all subreddits being scraped
for subr in all_subr:
    #output file
    file = open("../results/" + subr + ".jsonl","w")
    #fetch posts 
    for submission in tqdm.tqdm(reddit.subreddit(subr).hot(limit=100000)):
        #ignore posts without comments 
        if submission.num_comments < 1:
           continue
        title = submission.title
        post = submission.selftext
        author = check_valid(submission.author)
        submission.comments.replace_more(limit=0)
        comments = [{"comment_text":comment.body,"comment_author":check_valid(comment.author)} for comment in submission.comments.list()]
        obj = {"post_author":author,"post_text":post,"post_title":title,"post_comments":comments}
        file.write(str(json.dumps(obj)) + "\n")

