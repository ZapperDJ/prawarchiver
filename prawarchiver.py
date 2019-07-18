#! /usr/bin/env python
import praw
import pandas as pd
import time
from time import mktime
import datetime
import argparse
import os

reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')


def fetch_comments(topics_dict, path):
    id_list=topics_dict["id"]
    comments_dict = { "author":[], \
                "body":[], \
                "created_utc":[], \
                "id":[], \
                "link_id":[], \
                "parent_id": [], \
                "score":[], \
                "stickied":[], \
                "subreddit_id":[]}
    for id in id_list:
        print("Fetching comments for post " + id)
        submission = reddit.submission(id)
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()
        for comment in all_comments:
            comments_dict["author"].append(comment.author)
            comments_dict["body"].append(comment.body)
            comments_dict["created_utc"].append(int(comment.created_utc))
            comments_dict["id"].append(comment.id)
            comments_dict["link_id"].append(comment.link_id)
            comments_dict["parent_id"].append(comment.parent_id)
            comments_dict["score"].append(comment.score)
            comments_dict["stickied"].append(comment.stickied)
            comments_dict["subreddit_id"].append(comment.subreddit_id)
        comments_data = pd.DataFrame(comments_dict)
        comments_data.to_csv(path + '/' + id + '.csv', index=False) 
        comments_dict = { "author":[], \
                "body":[], \
                "created_utc":[], \
                "id":[], \
                "link_id":[], \
                "parent_id": [], \
                "score":[], \
                "stickied":[], \
                "subreddit_id":[]}

def fetch_links(subreddit=None, date_start=None, date_stop=None, limit=None):
    sr = reddit.subreddit(subreddit)
    subreddit_sort_new = sr.new(limit=int(limit))
    topics_dict = { "author":[], \
                    "created_utc":[], \
                    "domain":[], \
                    "id":[], \
                    "is_self":[], \
                    "num_comments": [], \
                    "over_18": [], \
                    "permalink":[], \
                    "retrieved_on":[], \
                    "score":[], \
                    "selftext":[], \
                    "stickied":[], \
                    "subreddit_id":[], \
                    "title":[], \
                    "url":[]}
    print('Fetching submissions %s to %s...' % (time.strftime('%Y-%m-%d', date_start), time.strftime('%Y-%m-%d', date_stop)))
    writing_day = None
    for submission in subreddit_sort_new:
        created_ts=int(submission.created_utc)
        date_start_ts=int(mktime(date_start)) - 86400 # make date inclusive, adjust for UTC
        date_stop_ts=int(mktime(date_stop)) + 86400
        if (created_ts > date_start_ts and created_ts < date_stop_ts): # check if post date is within specified captured range
            created_path = datetime.datetime.utcfromtimestamp(created_ts).strftime('%Y/%m/%d')
            topics_dict["author"].append(submission.author
)
            topics_dict["created_utc"].append(created_ts)
            topics_dict["domain"].append(submission.domain)
            topics_dict["id"].append(submission.id)
            topics_dict["is_self"].append(submission.is_self)
            topics_dict["num_comments"].append(submission.num_comments)
            topics_dict["over_18"].append(submission.over_18)
            topics_dict["permalink"].append(submission.permalink)
            topics_dict["retrieved_on"].append(int(time.time()))
            topics_dict["score"].append(submission.score)
            topics_dict["selftext"].append(submission.selftext)
            topics_dict["stickied"].append(submission.stickied)
            topics_dict["subreddit_id"].append(submission.subreddit_id)
            topics_dict["title"].append(submission.title)
            topics_dict["url"].append(submission.url)
            print('Fetching post ' + submission.id)
            if created_path != writing_day: # check if post date is different from previous post's date. If so, save links.csv and clear topics_dict
                writing_day = created_path
                path = 'data/' + subreddit + '/' + created_path
                os.makedirs(path, exist_ok=True)
                topics_data = pd.DataFrame(topics_dict)
                topics_data.to_csv(path + '/links.csv', index=False) 
                fetch_comments(topics_dict, path)
                topics_dict = { "author":[], \
                    "created_utc":[], \
                    "domain":[], \
                    "id":[], \
                    "is_self":[], \
                    "num_comments": [], \
                    "over_18": [], \
                    "permalink":[], \
                    "retrieved_on":[], \
                    "score":[], \
                    "selftext":[], \
                    "stickied":[], \
                    "subreddit_id":[], \
                    "title":[], \
                    "url":[]}
                
        else:
            print('Discarded post ' + submission.id + ': Out of date range' )

    
    
def mkdate(datestr):
  try:
    return time.strptime(datestr, '%Y-%m-%d')
  except ValueError:
    raise argparse.ArgumentTypeError(datestr + ' is not a proper date string')
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('subreddit', help='subreddit to archive')
    parser.add_argument('date_start', type=mkdate, help='start archiving at date, e.g. 2005-1-1')
    parser.add_argument('date_stop', type=mkdate, help='stop archiving at date, inclusive, cannot be date_start')
    parser.add_argument('--limit', default=1000, help='api limit param, default 100+0')
    args=parser.parse_args()

    args.subreddit = args.subreddit.lower()    
    
fetch_links(args.subreddit, args.date_start, args.date_stop, args.limit)
