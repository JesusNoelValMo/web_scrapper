
import argparse
import logging
import re
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
logging.basicConfig(level=logging.INFO)
from common import config
import news_page_object as news

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _news_scraper(news_site):
    host = config()['news_sites'][news_site]['url']
    logging.info('Beggning scrapper for {}'.format(host))
    homepage = news.HomePage(news_site, host)
    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site, host, link)
        if article:
            logger.info('Article fetched!!')
            articles.append(article)
            logger.info(article.title)
    print(len(article))

def _fetch_article(news_site, host, link):
    logger.info('Start fetching article at {}'.format(link))
    article = None
    try:
        article = news.ArticlePage(news_site, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warn('Error while fetching the article', exc_info=False)
    if article and not article.body:
        logger.warn('Invalid article, there is no body')
        return None
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{host}{uri}'.format(host=host, uri=link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


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


