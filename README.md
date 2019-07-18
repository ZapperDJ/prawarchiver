## prawarchiver

pulls data from the reddit api and renders offline compatible html pages

this is a fork of [reddit-html-archiver](https://github.com/libertysoft3/reddit-html-archiver), but it uses the reddit api (praw) instead of pushshift.io api (psaw)

### install

requires python 3 on linux, OSX, or Windows

    sudo apt-get install pip
    pip install psaw
    git clone https://github.com/chid/snudown
    cd snudown
    sudo python setup.py install
    cd ..
    git clone [this repo]
    cd reddit-html-archiver
    chmod u+x *.py

Windows users may need to run

    chcp 65001
    set PYTHONIOENCODING=utf-8

before running `prawarchiver.py` or `write_html.py` to resolve encoding errors such as 'codec can't encode character'.

### fetch reddit data

data is fetched by subreddit and date range and is stored as csv files in `data`.

    ./prawarchiver.py politics 2017-1-1 2017-2-1
    
**WARNING:** retrievable data is limited by reddit api to a max of 1000 posts

### write web pages

write html files for all subreddits to `r`.

    ./write_html.py
    # or add some output filtering
    ./write_html.py --min-score 100 --min-comments 100 --hide-deleted-comments
    ./write_html.py -h

your html archive has been written to `r`. once you are satisfied with your archive feel free to copy/move the contents of `r` to elsewhere and to delete the git repos you have created. everything in `r` is fully self contained.

to update an html archive, delete everything in `r` aside from `r/static` and re-run `write_html.py` to regenerate everything.

### hosting the archived pages

copy the contents of the `r` directory to a web root or appropriately served git repo.

### screenshots

![](screenshots/sub.jpg)
![](screenshots/post.jpg)
