import praw
import pandas as pd
# This file iterates through the top 5 comments of the top 100 posts in specified subreddit
# and appends it to a csv file


def scrape_comments(subreddit, comment_limit, no_posts):
    ls = []
    posts = subreddit.top("all")
    i = 0
    count = no_posts
    for post in posts:
        i += 1
        if i > count:
            break
        post.comment_sort = 'best'
        post.comment_limit = comment_limit
        for top_level_comment in post.comments:
            if isinstance(top_level_comment, praw.models.MoreComments):
                continue
            ls.append(post)
        df = pd.DataFrame(ls)
        df.to_csv('democrat100comments.csv', index=False)


reddit_read_only = praw.Reddit(client_id="Yq5U6qZg9bdz2hpfG_maWw",  # your client id
                               client_secret="VBlf2B7eWmM27gt0CilvSLx_kQPI_Q",  # your client secret
                               user_agent="HASS Scraping")  # your user agent
subreddit = reddit_read_only.subreddit("democrat")
scrape_comments(subreddit, 5, 100)
