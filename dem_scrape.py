from comment_scraper import *

max_posts = 5000
max_comments = 250
rep_subreddit = reddit_read_only.subreddit("democrats")
scrape_comments(
    rep_subreddit, max_comments, max_posts,
    export_name='dem-comments'
)
