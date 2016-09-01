
from flask import Flask, request, render_template

import sentiment
import tweets


STATE = sentiment.state_load()

app = application = Flask(__name__)


@app.route('/')
def index_page():
    q = request.args.get('q') or ''
    category = None
    if q:
        category = sentiment.get_text_category(STATE, q)

    return render_template('index.html', q=q, category=category)


@app.route('/tweets')
def tweets_page():
    q = request.args.get('q') or ''

    tweet_list = []
    if q:
        tweet_list = tweets.get_tweets(q)

    sent_list = [
        sentiment.get_text_category(STATE, tweet)
        for tweet in tweet_list
    ]

    pairs = zip(tweet_list, sent_list)

    return render_template('tweets.html', q=q, pairs=pairs)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=False)
