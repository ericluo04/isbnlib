# -*- coding: utf-8 -*-
"""Use Google to get an ISBN from words from title and author's name."""

import logging
from urllib.parse import quote

from ._core import get_canonical_isbn, get_isbnlike
from .dev import cache, webservice
# scraping
from bs4 import BeautifulSoup
import requests, random
import collections as c

LOGGER = logging.getLogger(__name__)


# extract plausible user agents (https://gist.github.com/6aditya8/c8ff33d6fc0c11de839bd9facf175cb6)
## scrape for a certain browser
def by_browser(browser):
    url = 'http://www.useragentstring.com/pages/useragentstring.php?name=' + browser
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    user_agent_links = soup.find('div', {'id': 'liste'}).findAll('a')[20:40]
    return [str(user_agent.text) for user_agent in user_agent_links]
## compile user agents
def get_user_agents():
    user_agents = []
    for browser in ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Edge', 'Internet Explorer', 'Opera']:
        user_agents.extend(by_browser(browser))
    return user_agents[3:] # Remove the first 3 Google Header texts from Chrome's user agents
# find user agents
proxy_user_agents = get_user_agents()
# remove invalid agents
user_agents = [i for i in proxy_user_agents if "More" not in i]
user_agents = [i.strip() for i in user_agents if len(i) >= 10]


@cache
def goos(words):
    """Use Google to get an ISBN from words from title and author's name."""
    service_url = 'http://www.google.com/search?q=ISBN+'
    search_url = service_url + quote(words.replace(' ', '+'))

    user_agent = random.choice(user_agents)

    content = webservice.query(
        search_url,
        user_agent=user_agent,
        appheaders={
            'Content-Type': 'text/plain; charset="UTF-8"',
            'Content-Transfer-Encoding': 'Quoted-Printable',
        },
    )
    isbns = get_isbnlike(content)
    isbn = ''
    try:
        for item in isbns:
            isbn = get_canonical_isbn(item, output='isbn13')
            if isbn:  # pragma: no cover
                break
    except IndexError:  # pragma: no cover
        pass
    if not isbns or not isbn:  # pragma: no cover
        LOGGER.debug('No ISBN found for %s', words)
    return isbn
