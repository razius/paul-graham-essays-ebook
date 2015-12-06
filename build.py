import io
import sys
import getopt
import shutil
import subprocess
import requests

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

BASE_URL = 'http://www.paulgraham.com'
IGNORED_TITLES = [
    'Chapter 1 of Ansi Common Lisp',
    'Chapter 2 of Ansi Common Lisp',
]


def get_page(page, download=False):
    if download:
        print 'Downloading page {}'.format(page)
        response = requests.get('{base_url}/{page}'.format(base_url=BASE_URL, page=page))
        content = response.text
        with io.open('download/{}'.format(page), 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        try:
            with io.open('download/{}'.format(page), 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError:
            return get_page(page, download=True)
    return content

def article_list(raw_page):
    soup = BeautifulSoup(raw_page, 'html.parser')
    link_elements = soup.find('img', alt='Essays').find_parent(
        'table').find_next_sibling('table').find_all('a')
    article_list = []
    for link_element in link_elements:
        title = link_element.contents[0]
        page = link_element.get('href')
        if title not in IGNORED_TITLES:
            article_list.append((title, page))
    return article_list


def article_content(raw_page):
    soup = BeautifulSoup(raw_page, 'html.parser')
    return soup.find('font', face='verdana').prettify()


if __name__ == '__main__':
    download = '--download' in sys.argv or '-d' in sys.argv

    article_list = article_list(get_page(page='articles.html', download=download))

    articles = []
    for title, page in article_list:
        content = article_content(get_page(page, download=download))
        articles.append((title, page, content))

    for static_file in ['cover.png', 'style.css']:
        shutil.copyfile(
            'static/{}'.format(static_file),
            'build/{}'.format(static_file)
        )

    env = Environment(loader=FileSystemLoader('templates'))
    for template in ['toc.html', 'book.ncx', 'book.opf', 'book.html']:
        with io.open('build/{}'.format(template), 'w', encoding='utf-8') as f:
            f.write(env.get_template(template).render(articles=articles))

    subprocess.call('kindlegen -c1 build/book.opf -o book.mobi', shell=True)
