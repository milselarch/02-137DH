import requests
import pandas as pd
# scrapes up to 100 posts from pushshift


def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.

    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.

    Read more: https://github.com/pushshift/api
    """

    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()


# Parameters
data_type = "comment"     # give me comments, use "submission" to publish something
# query = "python"  # query keyword
duration = "1825d"  # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
size = 1000  # maximum number of comments
sort_type = "score"  # Sort by score (Accepted: "score", "num_comments", "created_utc")
sort = "desc"  # sort descending
aggs = "subreddit"  #"author", "link_id", "created_utc", "subreddit"
subreddit = "republican"  # subreddit

data = get_pushshift_data(data_type=data_type,
                          after=duration,
                          size=size,
                          aggs=aggs,
                          sort=sort,
                          sort_type=sort_type,
                          subreddit=subreddit).get("data")

df = pd.DataFrame.from_records(data)[["body"]]
print(df.head)
print(df.columns)
