from __future__ import print_function

from six.moves.urllib.parse import quote_plus, urlencode
from six.moves.urllib.request import urlretrieve, urlopen
from six.moves.urllib.error import HTTPError
import feedparser

import xml.etree.ElementTree as ET
import datetime
import time
import sys


# URLs
OAI = '{http://www.openarchives.org/OAI/2.0/}'
ARXIV = '{http://arxiv.org/OAI/arXiv/}'
BASE = 'http://export.arxiv.org/oai2?verb=ListRecords&'

ARXIV_API = 'http://export.arxiv.org/api/'

def query(search_query="", id_list=[], prune=True, start=0, max_results=10):
    url_args = urlencode({"search_query": search_query,
                                 "id_list": ','.join(id_list),
                                 "start": start,
                                 "max_results": max_results})
    results = feedparser.parse(root_url + 'query?' + url_args)
    if results.get('status') != 200:
        # TODO: better error reporting
        raise Exception("HTTP Error " + str(results.get('status', 'no status')) + " in query")
    else:
        results = results['entries']
    for result in results:
        # Renamings and modifications
        mod_query_result(result)
        if prune:
            prune_query_result(result)
    return results

def mod_query_result(result):
    # Useful to have for download automation
    result['pdf_url'] = None
    for link in result['links']:
        if 'title' in link and link['title'] == 'pdf':
            result['pdf_url'] = link['href']
    result['affiliation'] = result.pop('arxiv_affiliation', 'None')
    result['arxiv_url'] = result.pop('link')
    result['title'] = result['title'].rstrip('\n')
    result['summary'] = result['summary'].rstrip('\n')
    result['authors'] = [d['name'] for d in result['authors']]
    if 'arxiv_comment' in result:
        result['arxiv_comment'] = result['arxiv_comment'].rstrip('\n')
    else:
        result['arxiv_comment'] = None
    if 'arxiv_journal_ref' in result:
        result['journal_reference'] = result.pop('arxiv_journal_ref')
    else:
        result['journal_reference'] = None
    if 'arxiv_doi' in result:
        result['doi'] = result.pop('arxiv_doi')
    else:
        result['doi'] = None

def prune_query_result(result):
    prune_keys = ['updated_parsed',
                  'published_parsed',
                  'arxiv_primary_category',
                  'summary_detail',
                  'author',
                  'author_detail',
                  'links',
                  'guidislink',
                  'title_detail',
                  'tags',
                  'id']
    for key in prune_keys:
        try:
            del result['key']
        except KeyError:
            pass

def to_slug(title):
    # Remove special characters
    filename = ''.join(c if c.isalnum() else '_' for c in title)
    # delete duplicate underscores
    filename = '_'.join(list(filter(None, filename.split('_'))))
    return filename

def download(obj, dirname='./', prepend_id=False, slugify=False):
    # Downloads file in obj (can be result or unique page) if it has a .pdf link
    if 'pdf_url' in obj and 'title' in obj and obj['pdf_url'] and obj['title']:
        filename = obj['title']
        if slugify:
            filename = to_slug(filename)
        if prepend_id:
            filename = obj['arxiv_url'].split('/')[-1] + '-' + filename
        filename = dirname + filename + '.pdf'
        # Download
        urlretrieve(obj['pdf_url'], filename)
        return filename
    else:
        print("Object obj has no PDF URL, or has no title")


class Record(object):
    '''
    A class to hold a single record from ArXiv
    Each records contains the following properties:

    object should be of xml.etree.ElementTree.Element.
    '''
    def __init__(self,xml_record):
        """if not isinstance(object,ET.Element):
            raise TypeError("")"""

        self.xml=xml_record
        self.id = self._get_text(ARXIV, 'id')
        self.title = self._get_text(ARXIV, 'title')
        self.abstract = self._get_text(ARXIV, 'abstract')
        self.cats = self._get_text(ARXIV, 'categories')
        self.created = self._get_text(ARXIV, 'created')
        self.updated = self._get_text(ARXIV, 'updated')
        self.doi = self._get_text(ARXIV, 'doi')
        self.authors = self._get_authors()

    def _get_text(self, namespace, tag):
        'Extracts text from an xml field'
        try:
            return self.xml.find(namespace + tag).text.strip()
        except:
            return ''

    def _get_authors(self):
        # authors
        authors = self.xml.findall(ARXIV+'authors/' + ARXIV + 'author')
        authors = [author.find(ARXIV+'keyname').text for author in authors]
        return authors

    def output(self):
        d = {'title': self.title,
            'id': self.id,
            'abstract': self.abstract,
            'categories': self.cats,
            'doi': self.doi,
            'created': self.created,
            'updated': self.updated,
            'authors': self.authors}
        return d

class Scraper(object):
    '''
    A class to hold info about attributes of scraping,
    such as date range, categories, and number of returned
    records. If `from` is not provided, the first day of
    the current month will be used. If `until` is not provided,
    the current day will be used.
    '''

    def __init__(self, category, date_from=None, date_until=None, t=30):
        self.cat = str(category)
        self.t = t
        #If from is not provided, use the first day of the current month.
        DateToday = datetime.date.today()
        if date_from is None:
            self.f = str(DateToday.replace(day=1))
        else:
            self.f = date_from
        #If date is not provided, use the current day.
        if date_until is None:
            self.u = str(DateToday)
        else:
            self.u = date_until
        self.url = (BASE + 'from=' + self.f + '&until=' + self.u +
                    '&metadataPrefix=arXiv&set=%s'%self.cat)

    def scrape(self):
        url = self.url
        ds = [] # collect all records in a list
        k=0
        while True:
            k+=1
            print ('fetching up to ', 1000*k, 'records...')
            try:
                response = urlopen(url)
            except HTTPError as e:
                # catch time error
                if e.code == 503:
                    to = int(e.hdrs.get("retry-after", 30))
                    print ("Got 503. Retrying after {0:d} seconds.".format(self.t))
                    time.sleep(to)
                    continue
                else:
                    raise

            xml = response.read()
            root = ET.fromstring(xml)
            records = root.findall(OAI + 'ListRecords/' + OAI + 'record')
            for record in records:
                meta = record.find(OAI+'metadata').find(ARXIV+"arXiv")
                record = Record(meta).output()
                ds.append(record)

            token = root.find(OAI+'ListRecords').find(OAI+"resumptionToken")
            if token is None or token.text is None:
                break
            else:
                url = (BASE + "resumptionToken=%s"%(token.text))

        print ('fetching is complete.')
        return ds

# get in categories with sapce, turn into a list
# -df date from, YYYY-MM-DD format
# -df date until, YYYY-MM-DD format
# check if df>di
