import sys
import simplejson
import re
from twython import Twython
import datetime

now = datetime.datetime.now()
filename = "twitter_data_%i.%i.%i.txt" % (now.month, now.day, now.year)

class MudScraper(object):
    API_URL = 'https://api.twitter.com/1.1/search/tweets.json'

    APP_KEY = 'doadCFjT8xKW1IKzzLC6kCr5K'
    APP_SECRET = 'qRNQvBxBXmL0b0bBTcnEONPQjDOwVjr7ubIwDd2UvDl5rAADYF'
    OAUTH_TOKEN = '155280821-tL4e8NIXIevgY4iZUW1okbudTaCCHRbGfvEuDan7'
    OAUTH_TOKEN_SECRET='zINzgGgArevnCSlhAAve086QAXnPI6mR6YFnxDU7x2QlW'

    def __init__(self):
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
        self.candidates = {}
        self.fields = set()
    
    def add_candidate(self, name, search_terms=[]):
        self.candidates[name] = Candidate(name, set(search_terms))

    def remove_candidate(self, name):
        del self.candidates[name]

    def add_search_terms(self, name, search_terms):
        self.candidates[name].add_search_terms(search_terms)

    def remove_search_terms(self, name, search_terms):
        self.candidates[name].remove_search_terms(search_terms)

    def get_tweets(self, name):
        search_terms = list(self.candidates[name].search_terms)
        status_texts = []
        for term in search_terms:
            query_results = self.twitter.search(q=term)
            # extracted_data = self.extract_data(query_results['statuses'])
            extracted_texts = self.extract_text(query_results['statuses'])
            status_texts.extend(extracted_texts)
        return status_texts

    def extract_text(self, statuses):
        return [remove_urls(s['text']) for s in statuses]

    def extract_data(self, statuses):
        def helper(status):
            data = {field: status[field] for field in self.fields if field in status.keys()}
        return [helper(status) for status in statuses]



class Candidate(object):
    def __init__(self, name):
        self.name = name
        self.search_terms = set()
        self.count = {'total': 0,
                      'positive': 0,
                      'negative': 0,
                      'neutral': 0}

    def add_search_terms(self, search_terms):
        self.search_terms = self.search_terms.union(set(search_terms))

    def remove_search_terms(self, search_terms):
        self.search_terms.difference_update(set(search_terms))


def remove_urls(text):
    return re.sub(r'(?:\@|https?\://)\S+', '', text)



# Tags to scrape
search_terms = ['Bernie Sanders', '#feelthebern']


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
