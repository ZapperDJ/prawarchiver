## Prawarchiver

Pulls data from the reddit api and renders offline compatible html pages

This is a fork of [reddit-html-archiver](https://github.com/libertysoft3/reddit-html-archiver), but it uses the reddit api (praw) instead of pushshift.io api (psaw)

### Install

Requires python 3 on linux, OSX, or Windows

    sudo apt-get install pip
    pip install praw
    pip install pandas
    git clone https://github.com/chid/snudown
    cd snudown
    sudo python setup.py install
    cd ..
    git clone [this repo]
    cd prawarchiver
    chmod u+x *.py

Windows users may need to run

    chcp 65001
    set PYTHONIOENCODING=utf-8

before running `prawarchiver.py` or `write_html.py` to resolve encoding errors such as 'codec can't encode character'.

A reddit api key is required to use prawarchiver. Create one here (script type) https://ssl.reddit.com/prefs/apps/ and fill this lines at the beginning whith your api keys

    reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')
              

### Fetch reddit data

Data is fetched by subreddit and date range and is stored as csv files in `data`.

    ./prawarchiver.py politics 2017-1-1 2017-2-1
    
**WARNING:** Retrievable data is limited by reddit api to a max of 1000 posts

### Write web pages

Write html files for all subreddits to `r`.

    ./write_html.py
    # or add some output filtering
    ./write_html.py --min-score 100 --min-comments 100 --hide-deleted-comments
    ./write_html.py -h

Your html archive has been written to `r`. Once you are satisfied with your archive feel free to copy/move the contents of `r` to elsewhere and to delete the git repos you have created. everything in `r` is fully self contained.

To update an html archive, delete everything in `r` aside from `r/static` and re-run `write_html.py` to regenerate everything.

### Hosting the archived pages

Copy the contents of the `r` directory to a web root or appropriately served git repo.

### screenshots

![](screenshots/sub.jpg)
![](screenshots/post.jpg)
