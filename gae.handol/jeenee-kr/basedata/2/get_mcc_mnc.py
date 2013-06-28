#!/usr/bin/python
# coding: utf-8
from BeautifulSoup import BeautifulSoup
import requests
import pandas as pd
import json
import re
import unidecode
import logging

logger = logging.getLogger(__name__)

CACHE_PATH = 'mcc_mnc'

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.;]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. Credit to Armin Ronacher from
    http://flask.pocoo.org/snippets/5/"""
    result = []
    text = text if isinstance(text, unicode) else text.decode('utf-8')
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode.unidecode(word).split())
    return unicode(delim.join(result))

def scrape():
    p = requests.get('http://www.mcc-mnc.com/')
    soup = BeautifulSoup(p.content)
    tb = soup.findAll('table', attrs={'id' : 'mncmccTable'})[0]
    soup = BeautifulSoup(p.content)
    tb = soup.findAll('table', attrs={'id' : 'mncmccTable'})[0]
    headers = [slugify(h.renderContents(), u'_') for h in tb.findAll('th')]
    rows = []
    for row_soup in tb.findAll('tr'):
        rows.append([c.renderContents() for c in row_soup.findAll('td')])

    # construct df and drop empty rows
    mcc_df = pd.DataFrame(rows, columns=headers)
    mcc_df = mcc_df.drop(0)

    # add custom fields
    mcc_df.mnc = ['0%s' % mnc if len(mnc) == 1 else '%s' % mnc for mnc in mcc_df.mnc]
    mcc_df['mcc_mnc'] = mcc_df.mcc.map(str) + '-' + mcc_df.mnc.map(str)
    mcc_df['slug'] = mcc_df.network.dropna().map(slugify) + '-' + mcc_df.country.dropna().map(slugify)
    mcc_df['name'] = mcc_df.network + ' ' + mcc_df.country
    mcc_df.iso = mcc_df.iso.apply(str.upper)
    logger.debug('mcc_df:\n%s', mcc_df[:10])
    return mcc_df

def export(mcc_df, cache_path=CACHE_PATH):
    mcc_df.to_csv(cache_path + '.csv', index=False)
    d_full = [r[1].to_dict() for r in mcc_df.iterrows()]
    json.dump(d_full, open(cache_path + '.json', 'w'), indent=2)
    d_min = dict(zip(mcc_df['mcc_mnc'],mcc_df['slug']))
    json.dump(d_min,  open(cache_path + '.min.json', 'w'), indent=2)

def mccmnc(usecache=False, cache_path=CACHE_PATH):
    mcc_df = None
    if usecache:
        try:
            mcc_df = pd.read_csv(cache_path + '.csv')
        except:
            pass
    if mcc_df is None:
        mcc_df = scrape()
        mcc_df.to_csv(cache_path + '.csv', index=False)
    return [r[1].to_dict() for r in mcc_df.iterrows()]

def main():
    mcc_df = scrape()
    export(mcc_df)

if __name__ == '__main__':
    main()
