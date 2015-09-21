
class Candidate(object):
    def __init__(self, name, search_terms):
        self.name = name
        self.search_terms = set(search_terms)
        self.count = {'total': 0,
                      'positive': 0,
                      'negative': 0,
                      'neutral': 0}
        self.confidence = {'total': 0.0,
                      'positive': 0.0,
                      'negative': 0.0,
                      'neutral': 0.0}

    def update_count(self, neu_count, neg_count, pos_count):
        self.count['total'] += neu_count + neg_count + pos_count
        self.count['neutral'] += neu_count
        self.count['negative'] += neg_count
        self.count['positive'] += pos_count

    def update_confidence(self, neu_count, neg_count, pos_count):
        self.confidence['total'] += neu_conf + neg_conf + pos_conf
        self.confidence['neutral'] += neu_conf
        self.confidence['negative'] += neg_conf
        self.confidence['positive'] += pos_conf

    def add_search_terms(self, search_terms):
        self.search_terms = self.search_terms.union(set(search_terms))

    def remove_search_terms(self, search_terms):
        self.search_terms.difference_update(set(search_terms))

