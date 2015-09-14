import sys
import simplejson
from twython import Twython
import datetime

now = datetime.datetime.now()
filename = "twitter_data_%i.%i.%i.txt" % (now.month, now.day, now.year)
APP_KEY = 'doadCFjT8xKW1IKzzLC6kCr5K'
APP_SECRET = 'qRNQvBxBXmL0b0bBTcnEONPQjDOwVjr7ubIwDd2UvDl5rAADYF'
OAUTH_TOKEN = '155280821-tL4e8NIXIevgY4iZUW1okbudTaCCHRbGfvEuDan7'
OAUTH_TOKEN_SECRET='zINzgGgArevnCSlhAAve086QAXnPI6mR6YFnxDU7x2QlW'

twitter = Twython(APP_KEY, APP_SECRET,
        oauth_token=OAUTH_TOKEN, oauth_token_secret=OAUTH_TOKEN_SECRET)

ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
# Tags to scrape
tags = ['Bernie Sanders', '#feelthebern']

t = Twython(app_key='doadCFjT8xKW1IKzzLC6kCr5K',
            app_secret='qRNQvBxBXmL0b0bBTcnEONPQjDOwVjr7ubIwDd2UvDl5rAADYF',
            oauth_token='155280821-tL4e8NIXIevgY4iZUW1okbudTaCCHRbGfvEuDan7',
            oauth_token_secret='zINzgGgArevnCSlhAAve086QAXnPI6mR6YFnxDU7x2QlW')

# IDs to scrape
ids = "4816, 9715012"

# Looks up users
users = t.lookup_user(user_id=ids)

# USERS RETURNED AS JSON OBJECTS
outfn = "twitter_user_data_%i.%i.%i.txt" % (now.month, now.day, now.year)

fields = "id screen_name name created_at url followers_count friends_count statuses_count \
        favourites_count listed_count \
        contributors_enabled description protected location lang expanded_url".split()

outfp = open(outfn, 'w')
outfp.write(''.join(fields, '\t') + '\n') # Header

for entry in users:
    r = {}
    for f in fields:
        r[f] = ''
    r['id'] = entry['id']
    r['screen_name'] = entry['screen_name']
    r['name'] = entry['name']
    r['created_at'] = entry['created_at']
    r['url'] = entry['url']
    r['followers_count'] = entry['followers_count']
    r['friends_count'] = entry['friends_count']
    r['statuses_count'] = entry['statuses_count']
    r['favourites_count'] = entry['favourites_count']
    r['listed_count'] = entry['listed_count']
    r['contributors_enabled'] = entry['contributors_enabled']
    r['description'] = entry['description']
    r['protected'] = entry['protected']
    r['location'] = entry['location']
    r['lang'] = entry['lang']
    if 'url' in entry['entities']:
        r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
    else:
        r['expanded_url'] = ''
    print r

    lst = []
    for f in fields:
        lst.append(unicode(r[f]).replace('\/','/'))
    outfp.write(''.join(lst, '\t').encode('utf-8') + '\n')

outfp.close()
