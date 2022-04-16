from psaw import PushshiftAPI
import csv

api = PushshiftAPI()
gen = api.search_comments(subreddit='democrat', limit=10)

with open('reddit_analysis.csv', 'w', newline='') as csvfile:
    writerobj = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for comment in gen:
        writerobj.writerow([comment.id, comment.author, comment.score, comment.permalink, comment.subreddit])
