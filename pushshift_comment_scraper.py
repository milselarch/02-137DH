import pandas as pd
import datetime as dt
from pmaw import PushshiftAPI

api = PushshiftAPI()

before = int(dt.datetime(2022, 4, 23, 0, 0).timestamp())
after = int(dt.datetime(2018, 10, 10, 0, 0).timestamp())
subreddit = "conservative"
limit = 100

comments = api.search_comments(subreddit=subreddit, limit=limit, before=before, after=after)
comments_df = pd.DataFrame(comments)
comments_df = comments_df[["body"]]
print(comments_df.columns)
comments_df.to_csv('datasets/republican_comments_pushshift.csv', header=True, index=False, columns=list(comments_df.axes[1]))
