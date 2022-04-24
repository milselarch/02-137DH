import praw
import pandas as pd

from datetime import datetime
from tqdm import tqdm
from time import sleep

# This file iterates through the top
# comments of the top posts in specified subreddit
# and appends it to a csv file


def scrape_comments(
    subreddit, comment_limit, num_posts,
    export_dir='datasets', export_name='rep_comments',
    stamp=None
):
    if stamp is None:
        date = datetime.now()
        stamp = date.strftime('%y%m%d-%H%M')

    export_path = f'{export_dir}/{export_name}-{stamp}.csv'
    print(f'export path = {export_path}')

    post_urls, post_ids = [], []
    comments, comment_ids = [], []
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

        for comment in post.comments:
            num_comments += 1
            if isinstance(comment, praw.models.MoreComments):
                continue

            post_ids.append(post.id)
            post_urls.append(post.url)
            comments.append(comment.body)
            comment_ids.append(comment.id)
            pbar.set_description(f'comments: {num_comments}')

        sleep(0.1)

    df = pd.DataFrame({
        'post_url': post_urls, 'post_id': post_ids,
        'comment': comments, 'comment_id': comment_ids
    })

    df.to_csv(export_path, index=False)
    print(f'exported to {export_path}')


reddit_read_only = praw.Reddit(
    client_id="Yq5U6qZg9bdz2hpfG_maWw",  # your client id
    client_secret="VBlf2B7eWmM27gt0CilvSLx_kQPI_Q",  # your client secret
    user_agent="HASS Scraping"  # your user agent
)

if __name__ == '__main__':
    max_posts = 5000
    max_comments = 250
    rep_subreddit = reddit_read_only.subreddit("republican")
    scrape_comments(
        rep_subreddit, max_comments, max_posts,
        export_name='rep_comments'
    )
