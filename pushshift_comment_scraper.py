import pandas as pd
import datetime as dt
from pmaw import PushshiftAPI

# pmaw scraper that can scrape >1000 posts/submissions

api = PushshiftAPI()

# parameters
before = int(dt.datetime(2022, 4, 23, 0, 0).timestamp())
after = int(dt.datetime(2018, 10, 10, 0, 0).timestamp())
subreddit = "republican"
limit = 100000

duration = "1825d"  # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
sort_type = "score"  # Sort by score (Accepted: "score", "num_comments", "created_utc")
sort = "desc"  # sort descending


comments = api.search_comments(subreddit=subreddit, limit=limit, after=after, sort=sort, sort_type=sort_type)
comments_df = pd.DataFrame(comments)
comments_df = comments_df[["body"]]
print(comments_df.columns)
print(comments_df.size)
comments_df.to_csv('datasets/republican_topcomments_100000.csv', header=True, index=False, columns=list(comments_df.axes[1]))
