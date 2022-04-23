import praw
import pandas as pd

from tqdm import tqdm

# This file iterates through the top
# comments of the top posts in specified subreddit
# and appends it to a csv file


def scrape_comments(
    subreddit, comment_limit, num_posts,
    export_path='datasets/republican_comments.csv'
):
    post_urls, post_ids, comments = [], [], []
    posts = subreddit.top(limit=num_posts)
    # count = num_posts

    num_comments, k = 0, 0
    pbar = tqdm(range(num_posts))

    for post in posts:
        # k += 1
        # if k > count:
        #     print('max posts reached')
        #     break

        pbar.update(1)
        post.comment_sort = 'best'
        post.comment_limit = comment_limit

        for top_level_comment in post.comments:
            num_comments += 1
            if isinstance(top_level_comment, praw.models.MoreComments):
                continue

            post_ids.append(post.id)
            post_urls.append(post.url)
            comments.append(top_level_comment.body)
            pbar.set_description(f'comments: {num_comments}')

    df = pd.DataFrame({
        'post_url': post_urls, 'post_id': post_ids,
        'comment': comments
    })

    df.to_csv(export_path, index=False)
    print(f'exported to {export_path}')


reddit_read_only = praw.Reddit(
    client_id="Yq5U6qZg9bdz2hpfG_maWw",  # your client id
    client_secret="VBlf2B7eWmM27gt0CilvSLx_kQPI_Q",  # your client secret
    user_agent="HASS Scraping"  # your user agent
)

max_posts = 5000
max_comments = 100
rep_subreddit = reddit_read_only.subreddit("republican")
scrape_comments(rep_subreddit, max_comments, max_posts)
