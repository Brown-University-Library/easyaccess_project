# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import httplib2
import logging, os, pprint, urllib
from datetime import datetime
import hmac
import base64
import hashlib
# from pprint import pprint
import json
import requests
import sys

api_id = os.environ['EZACS__SUMMON_API_ID']
api_key = os.environ['EZACS__SUMMON_API_KEY']

log = logging.getLogger('access')
log.debug( 'summon.py loaded' )


class SummonSearch(object):
    def __init__(self, api_id, api_key):
        log.debug( 'SummonSearch instantiated' )
        self.api_id = api_id
        self.api_key = api_key
        self.host = 'api.summon.serialssolutions.com'
        self.path = '/2.0.0/search'
        self.accept = 'application/json'

    def make_headers(self, query):
        """
        Search Summon API with Python.
        See Dough Chesnut's Code4Lib mailing list post: http://serials.infomotions.com/code4lib/archive/2010/201010/2408.html
        """
        summonAccessID = self.api_id
        summonSecretKey = self.api_key
        summonAccept = self.accept
        summonThedate = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        summonQS = "&".join(sorted(query.split('&')))
        summonQS = urllib.unquote_plus(summonQS)
        summonIdString = summonAccept + "\n" + summonThedate + "\n" + self.host + "\n" + self.path + "\n" + summonQS + "\n"
        summonDigest = base64.encodestring(hmac.new(summonSecretKey, unicode(summonIdString), hashlib.sha1).digest())
        summonAuthstring = "Summon "+summonAccessID+';'+summonDigest
        summonAuthstring = summonAuthstring.replace('\n','')
        return {'Accept':summonAccept,
                'x-summon-date':summonThedate,
                'Host':self.host,
                'Authorization':summonAuthstring}

    def fetch(self, query):
        #Set a timeout for the Summon request.
        http = httplib2.Http(timeout=10)
        headers = self.make_headers(query)
        url = 'http://%s%s?%s' % (self.host, self.path, query)
        response, content = http.request(url, 'GET', headers=headers)
        try:
            out = json.loads(content)
        except ValueError:
            return None
        return out

class SummonResponse(object):
    def __init__(self, response):
        log.debug( 'SummonResponse instantiated' )
        self.response = response

    @property
    def numFound(self):
        c = self.response['recordCount']
        if c == '':
            return 0
        else:
            return c

    def query(self):
        return self.response['query']

    @property
    def echoedQuery(self):
        q = self.query()
        return q.get('queryString', '')

    def docs(self):
        if self.response is None:
            return []
        return self.response['documents']



def summon_citation(doc):
    """
    Turn a Summon response into a normalized 'citation' that matches
    responses from other systems.
    """

    def _format(value):
        if value == 'Journal Article':
            return 'journal'
        return value

    def _g(doc, item):
        """
        Helper to get the first item in the list if it exists.
        """
        try:
            return doc.get(item, [''])[0]
        except IndexError:
            return ''

    return {
            'format': _format(_g(doc, 'ContentType')),
            'citation': {
                'source': _g(doc, 'PublicationTitle'),
                'title': _g(doc, 'Title'),
                #First creator only.
                'creator': _g(doc, 'Author'),
                'volume': _g(doc, 'Volume'),
                'issue': _g(doc, 'Issue'),
                'pmid': _g(doc, 'PMID'),
                'doi': _g(doc, 'DOI'),
                'issn': _g(doc, 'ISSN'),
                'date': _g(doc, 'PublicationYear'),
                'isbn': doc.get('ISBN', []),
                'held': doc.get('inHoldings', False),
                'abstract': _g(doc, 'Abstract'),
                'date': _g(doc, 'PublicationDate')
                },
            'openurl': doc.get('openUrl', ''),
    }

def get_summon_enhanced_link(qtype, value):
    log.debug( 'starting get_summon_enhanced_link()' )
    link = None
    if qtype == 'doi':
        q = 's.q=' + 'DOI:"%s"' % value.replace('/', '%2F')
    elif qtype == 'pmid':
        q = 's.q=' + 'PMID:"%s"' % value
    else:
        raise Exception("Invalid Summon query type.  Must be DOI or PMID. %s received." % qtype)
    session = SummonSearch(api_id, api_key)
    resp = session.fetch(q)
    if resp is None:
        return
    docs = SummonResponse(resp).docs()
    log.debug( 'summon docs, ```{}```' )
    try:
        doc = docs[0]
    except IndexError:
        return
    if doc.get('inHoldings') == True:
	if doc.get('LinkModel', ['null'])[0] == "DirectLink":
	    link = doc.get('link')
    return link

def get_enhanced_link(query_string):
    """
    This will attempt to find a best bet link via Summon
    and send the user there before hitting the 360Link
    API.
    """
    log.debug( 'starting get_enhanced_link()' )
    from bibjsontools import from_openurl
    link = None
    bib = from_openurl(query_string)
    #Get referrer.
    rfr = bib.get('_rfr')
    log.debug( 'rfr, `{}`'.format(rfr) )
    #Skip summon requests because they have already been
    #enhanced by the index.
    if rfr != 'info:sid/summon.serialssolutions.com':
        for ident in  bib.get('identifier', []):
            if ident['type'] == 'doi':
                doi = ident['id'].lstrip('doi:')
                link = get_summon_enhanced_link('doi', doi)
            elif ident['type'] == 'pmid':
                pmid = ident['id'].lstrip('info:pmid/')
                link = get_summon_enhanced_link('pmid', pmid)
            if link:
                return link
    return

def get_brown_proxy_link(summonlink):
    """
    Submit a head request to the link and follow the redirects.

    Return the link that has either the Brown proxy URL or
    is the firs link after the serials solutions hashed link.

    """
    resp = requests.head(summonlink)
    #Store a best bet if something doesn't work with fetching the url
    best = summonlink
    for index, h in enumerate(resp.history):
        url = h.url
        #print>>sys.stderr, '*****', url
        #If we have followed a link this far, it's now the best bet.
        if index == 1:
            best = url
        if url.find('revproxy.brown.edu') > 0:
            return url
    return best


import unittest
class TestSummon(unittest.TestCase):

    def test_pmid_query(self):
        q = 's.q=' + urllib.quote_plus('PMID:"%s"' % '20687839')
        sum = SummonSearch(api_id, api_key)
        resp = sum.fetch(q)
        sum = SummonResponse(resp)
        docs = sum.docs()
        doc = docs[0]
        self.assertTrue(doc['Title'], "Not All Patients with Vancomycin-Resistant Enterococci Need To Be Isolated")
        self.assertTrue("1058-4838" in doc['ISSN'])
        #pprint(summon_citation(doc))

    def test_doi_query(self):
        doi = '10.1002/cne.22033'
        q = 's.q=' + 'DOI:"%s"' % doi.replace('/', '%2F')
        sum = SummonSearch(api_id, api_key)
        resp = sum.fetch(q)
        sum = SummonResponse(resp)
        docs = sum.docs()
        doc = docs[0]
        self.assertTrue("0021-9967" in doc['ISSN'])

    def test_doi_query_enhanced_link(self):
        qstring = 'doi=10.1002/cne.22033'
        link = get_enhanced_link(qstring)
        self.assertTrue(link is None)
        qstring = 'doi=10.1016/S1532-0464(02)00004-7&rfr_id=info:sid/summon.serialssolutions.com'
        link = get_enhanced_link(qstring)
        if link:
            resp = requests.get(link)
            for h in resp.history:
                print h, h.url
        self.assertTrue(link is None)

    def test_enhanced_link_full_openurl_with_doi_in_holdings(self):
        """
        Link hashes seem to change.  Verify that brown.summon is in response for fetched links.
        """
        qstring = 'rft.eissn=1532-2548&rft_id=info:doi/10.1104/pp.65.2.211&rft.au=Richmond, P. A.&rft.aulast=Richmond&rft.volume=65&rft.jtitle=Plant physiology (Bethesda)&rft.aufirst=P. A.&rft.date=1980-02&rft.atitle=Cell Expansion Patterns and Directionality of Wall Mechanical Properties in Nitella.&rft.spage=211&rft.issue=2&rft.issn=0032-0889&url_ver=Z39.88-2004&version=1.0&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.genre=article HTTP/1.1" 200 2507 "http://library.brown.edu/easyarticle/?&url_ver=Z39.88-2004&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.atitle=CELL EXPANSION PATTERNS AND DIRECTIONALITY OF WALL MECHANICAL-PROPERTIES IN NITELLA&rft.aufirst=PA&rft.aulast=RICHMOND&rft.date=1980&rft.epage=217&rft.genre=article&rft.issn=0032-0889&rft.issue=2&rft.jtitle=PLANT PHYSIOLOGY&rft.pages=211-217&rft.spage=211&rft.stitle=PLANT PHYSIOL&rft.volume=65&rfr_id=info:sid/www.isinet.com:WoK:WOS&rft.au=METRAUX, JP&rft.au=TAIZ, L&rft_id=info:doi/10.1104/pp.65.2.211'
        link = get_enhanced_link(qstring)
        self.assertTrue(link.find('brown.summon') > 0)

    def test_enhanced_link_open_access(self):
        """
        http://api.summon.serialssolutions.com/help/api/search/example?s_q=DOI:10.1158/1078-0432.CCR-07-4496
        """
        qstring = 'url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&__char_set=utf8&rft_id=info:doi/10.1158/1078-0432.CCR-07-4496&rfr_id=info:sid/libx%3Abrown&rft.genre=article'
        link = get_enhanced_link(qstring)
        self.assertTrue(link.find('brown.summon') > 0)

    def test_enhanced_link_not_held(self):
        qstring = 'rft_id=info:doi/10.3109/15563650.2012.748194'
        link = get_enhanced_link(qstring)
        self.assertFalse(link)

    def test_enhanced_link_pmid_not_held(self):
        qstring = 'id=pmid:8593094'
        link = get_enhanced_link(qstring)
        self.assertFalse(link)

    def test_enhanced_link_pmid_held_openurl(self):
	"""
	This link leads to an OpenURL via LinkModel
	"""
        qstring = 'id=pmid:7593094'
        link = get_enhanced_link(qstring)
	self.assertFalse(link)
        #print get_brown_proxy_link(link)

    def test_enhanched_link_pmid_direct(self):
	qstring = 'id=pmid:8205861'
	link = get_enhanced_link(qstring)
	self.assertTrue(link.find('brown.summon') > 0)




if __name__ == '__main__':
    unittest.main()
