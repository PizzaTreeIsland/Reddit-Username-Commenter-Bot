import praw
import datetime
import re
import time

# Reddit API Credentials
reddit = praw.Reddit(
    client_id="CLIENT-ID",
    client_secret="CLIENT-SECRET",
    user_agent="UserNameCommenter v. 0.2 by u/UsernameCommenterBot",
    username="UsernameCommenterBot",
    password="PASSWORD"
)

# List of subreddits to monitor
with open(r"subredditlist.txt", "r") as listfile:
    subreddits_to_monitor = [line.strip() for line in listfile.readlines()]

subreddits_to_monitor=subreddits_to_monitor[:600:] #rate limiting to avoid api errors. Can be resolved by parrallelizing.


target_string = "u/"


def post_comment(post):
    usernames=re.findall(r"u/(\S+)", post.title)
    usernames=[f"u/{name}" for name in usernames]

    if len(usernames)==1:
        post.reply(f"It seems you mentioned {usernames[0]} in your submission title. I mentioned them here so mobile users can easily click on the name. I am a bot. If I did something wrong, please message me. ")
        print(f"{datetime.datetime.now()}: Found post {post.title} and commented username {usernames[0]}. {post.shortlink}")
    elif len(usernames)>1:
        post.reply(f"It seems you mentioned the following users in your submission title: \n {', '.join(usernames)}\nI mentioned them here so mobile users can easily click on the name. I am a bot. If I did something wrong, please message me. ")
        print(f"{datetime.datetime.now()}: Found post {post.title} and commented these usernames: {', '.join(usernames)}. {post.shortlink}")
    else: 
        print(f"{datetime.datetime.now()}: Found post {post.title} but couldn't find an usernames. {post.shortlink}")
        
# Monitor new posts
subreddit = reddit.subreddit("+".join(subreddits_to_monitor))
def monitor():
    global subreddit
    global target_string
    global reddit
    try: 
        for post in subreddit.stream.submissions(skip_existing=True):
            if target_string.lower() in post.title.lower():
                post_comment(post)
    except: 
        print("An error occured. Trying again in 10seconds")
        time.sleep(10)
        monitor()
        
monitor()
