import sys
import simplejson
import re
from twython import Twython
import datetime
import unirest
from candidate import Candidate

API_URL = 'https://api.twitter.com/1.1/search/tweets.json'

APP_KEY = 'doadCFjT8xKW1IKzzLC6kCr5K'
APP_SECRET = 'qRNQvBxBXmL0b0bBTcnEONPQjDOwVjr7ubIwDd2UvDl5rAADYF'
OAUTH_TOKEN = '155280821-tL4e8NIXIevgY4iZUW1okbudTaCCHRbGfvEuDan7'
OAUTH_TOKEN_SECRET='zINzgGgArevnCSlhAAve086QAXnPI6mR6YFnxDU7x2QlW'


class MudScraper(object):

    def __init__(self):
        self.twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.candidates = {}
        self.fields = set(['place'])
    
    def add_candidate(self, name, search_terms=[]):
        self.candidates[name] = Candidate(name, search_terms + [name])

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
#            print term
            query_results = self.twitter.search(q=term)
            extracted_data = self.extract_data(query_results['statuses'])
            extracted_texts = self.extract_text(query_results['statuses'])
            status_texts.extend(extracted_texts)
#            print 'coordinates', query_results['statuses'][0]['coordinates']
        return status_texts

    def extract_text(self, statuses):
        return [self._strip_retweet_text(remove_urls(s['text'])) for s in statuses]

    def extract_data(self, statuses):
        def helper(status):
            data = {field: status[field] for field in self.fields if field in status.keys()}
        return [helper(status) for status in statuses]

    def get_sentiment(self, text):
        response = unirest.post("https://community-sentiment.p.mashape.com/text/",
                        headers={
                            "X-Mashape-Key": "45azK9j34umshjwdrcnjRgJJRtC0p13dgPVjsnlPW8IqE5hEl5",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "application/json"
                        },
                        params={
                            "txt": text
                        }
                    )
#        return response.body
        return response.body['result'] if response != None else None

    def analyze_texts(self, name, texts):
        stats = [self.get_sentiment(text) for text in texts]
        neu_conf, neu_count = self.average_sentiment_confidence(stats)
        neg_conf, neg_count = self.average_sentiment_confidence(stats, 'Negative')
        pos_conf, pos_count = self.average_sentiment_confidence(stats, 'Positive')
        total_conf, total_count = self.total_average_confidence(stats)
        self.candidates[name].update_count(neu_count, neg_count, pos_count)
        self.candidates[name].update_confidence(neu_conf, neg_conf, pos_conf)

        # print self.average_sentiment_confidence(stats)
        #print self.average_sentiment_confidence(stats, 'Negative')
        #print self.average_sentiment_confidence(stats, 'Positive')
        #print '(%s, %s)' % (total_conf, total_count)

    def average_sentiment_confidence(self, stats, sentiment='Neutral'):
        conf = [float(s['confidence']) for s in stats if s['sentiment'] == sentiment]
        return (sum(conf) / len(conf), len(conf))

    def total_average_confidence(self, stats):
        conf = [float(s['confidence']) for s in stats]
        return (sum(conf) / len(conf), len(conf))
        

    def _strip_retweet_text(self, text):
        """ Very rudimentary removal of 'RT' at the start of 
        status strings. TODO: Improve this shit.
        """
        return text[4:] if text[:4] == 'RT  ' else text

def remove_urls(text):
    return re.sub(r'(?:\@|https?\://)\S+', '', text)
