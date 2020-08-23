
import argparse
import logging
logging.basicConfig(level=logging.INFO)
from common import config
import news_page_object as news

logger = logging.getLogger(__name__)

def _news_scraper(news_site):
    host = config()['news_sites'][news_site]
    logging.info('Beggning scrapper for {}'.format(host))
    homepage = news.HomePage(news_site, host)
    for link in homepage.article_links:
        print(link)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_sites'].keys())
    print(news_site_choices)
    parser.add_argument("news_site",
                        help= "the news site",
                        type=str,
                        choices=news_site_choices)
    args = parser.parse_args()
    _news_scraper(args.news_site)


