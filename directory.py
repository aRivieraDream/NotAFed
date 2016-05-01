from flask import Flask, render_template, request
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime
import Bach as b

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def form_d_filings():
    return render_template('index.html')

def make_external(url):
    return urljoin(request.url_root, url)


@app.route('/dRSS')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    query = b.form_d_query()
    filings = b.get_last_ten(query)
    for filing in filings:
        print '\n\n\n---------------------'
        print filing['uid']
        print filing['title']
        print filing['story']
        print '\n\n\n---------------------'
        feed.add(filing['title'], unicode(filing['story']),
                 content_type='html',
                 url=make_external(filing['url']),
                 updated=filing['pubDate'])
    return feed.get_response()


if __name__ == "__main__":
    app.run(debug=True) #remove debug function later
