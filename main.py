from scraper import MudScraper

def main(args):
    M = MudScraper()
    M.add_candidate('Bernie Sanders', ['#feelthebern'])
    M.get_tweets('Bernie Sanders')


if __name__ == '__main__':
    main(sys.argv[1:])
