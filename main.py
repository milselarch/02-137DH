import praw
import pandas as pd
# test

reddit_read_only = praw.Reddit(
    client_id="Yq5U6qZg9bdz2hpfG_maWw",  # your client id
    client_secret="VBlf2B7eWmM27gt0CilvSLx_kQPI_Q",  # your client secret
    user_agent="HASS Scraping"  # your user agent
)

subreddit = reddit_read_only.subreddit("democrat")

posts = subreddit.top("all")
# Scraping the top posts of the current month
posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": []
              }
i = 0
count = 100
for post in posts:
    i += 1
    if i > count:
        break

    # Title of each post
    posts_dict["Title"].append(post.title)
    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)
    # Unique ID of each post
    posts_dict["ID"].append(post.id)
    # The score of a post
    posts_dict["Score"].append(post.score)
    # Total number of comments inside the post
    posts_dict["Total Comments"].append(post.num_comments)
    # URL of each post
    posts_dict["Post URL"].append(post.url)

# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv("democrat100.csv", index=True)
