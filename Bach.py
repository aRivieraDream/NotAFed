# Takes crawler data from RTS and creates an RSS feed.
#TODO Use flask to publish feed
#TODO Store time of most recent post for referencing in query
import pymssql
import creds

# query for form d's from replica
def form_d_query():
    """Consider using variables to change things like # rows and form type"""
    return """
    select top 10
        t.entityid
        , t.name
        , t.createdat
        , t.roundamount
        , t.existinrts
        , tf.[file] as [file]
        , tf.size
    from task t
        inner join taskfile tf on tf.taskid = t.entityid
    where t.type in (1, 2, 13, 14) --form d
    order by t.createdat desc
    """


# prep creds and create cursor please don't forget to close cursor after using
def get_cursor():
    server = creds.server
    user = creds.user
    password = creds.creds
    db = creds.db
    encode = 'UTF-8'
    conn = pymssql.connect(server=server, user=user, password=password, database=db, charset=encode)
    cursor = conn.cursor()
    return cursor


# create a list of stories out of form d filings
def get_last_ten(query):
    c = get_cursor()
    c.execute(query)
    filings = []
    row = c.fetchone()
    while row:
        story = {'title':row[1], 'story':row[5], 'pubDate':row[2], 'uid':row[0]}
        start_key = 'Link to Form D: <a href=\''
        end_key = 'primary_doc.xml'
        start_loc = row[5].find(start_key)
        end_loc = row[5].find(end_key)
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=d&owner=include&count=40&action=getcurrent'
        if start_loc > 0:
            url = row[5][start_loc + len(start_key):end_loc + len(end_key)]
            print url
            story['url'] = url
        filings.append(story)
        row = c.fetchone()
    return filings


if __name__ == "__main__":
    encode = 'UTF-8'
    # conn = pymssql.connect(server=server, user=user, password=creds, database=db, charset=encode)
    # cursor = conn.cursor()
    # cursor.execute(query())
    # row = cursor.fetchone()
