import sys
from scraper import MudScraper

def main(args):
    M = MudScraper()
    M.add_candidate('Bernie Sanders', ['#feelthebern'])
    texts = M.get_tweets('Bernie Sanders')
    for t in texts:
        print t


if __name__ == '__main__':
    main(sys.argv[1:])
