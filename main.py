from scraper import MudScraper
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    M = MudScraper()
    name = 'Bernie Sanders'
    M.add_candidate(name , ['#feelthebern'])#, '#vets4bernie', '#bernie2016', '#bernieinva'])
    texts = M.get_tweets(name)
    texts = [t.encode('ascii', 'ignore') for t in texts]
    #for t in texts:
    #    print '\n************'
    #    print t, '\n -----'
    #    print M.get_sentiment(t)
    #    print '************'
    #M.analyze_texts(name, texts)
    #return M.candidates[name].confidence['total']
    return 'SUP DOGCAT'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run()

