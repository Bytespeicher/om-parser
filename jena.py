#!/usr/local/bin/python2.7
# -*- encoding: utf-8 -*-
#
# A Studentenwerk Thüringen Mensa scraper, producing XML for openMensa.

import sys
import urllib2


MENSEN = {
    'Ernst-Abbe-Platz': '/deutsch/mensen/einrichtungen/jena/mensa-ernst-abbe-platz.html',
    'Philosophenweg': '/deutsch/mensen/einrichtungen/jena/mensa-philosophenweg.html',
    'Carl-Zeiss-Promenade': '/deutsch/mensen/einrichtungen/jena/mensa-carl-zeiss-promenade.html'
}


def get(uri='/'):
    """A wrapper for GET-requests to www.stw-thueringen.de."""

    req = urllib2.Request(
        'http://www.stw-thueringen.de' + uri,
        headers={'User-Agent': "Mozilla/5.0 Gecko/20120427 Firefox/15.0"}
    )

    try:
        resp = urllib2.urlopen(req, timeout=10)
    except (urllib2.URLError, urllib2.HTTPError) as e:
        raise

    return resp.code, resp.read()


def extract(html):
    """Extract meals from HTML and yielding them as dictlike-object."""

    i, j = html.find('<table'), html.find('</table>')
    html = html[i:j] + '</table>'

    name = 'Foo'
    date = 'Heute'
    category = 'Essen 3.14'
    description = 'mit Gehirn'

    yield type('Meal', (object, ), {
        'name': name,
        'date': date,
        'category': category,
        'description': description,
        '__getitem__': lambda cls, item: getattr(cls, item)
    })()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: %s MENSA' % sys.argv[0]
        sys.exit(1)

    try:
        mensa = [key for key in MENSEN if key.lower().startswith(sys.argv[1].lower())][0]
    except IndexError:
        print '%s is not available. Try %s' % (sys.argv[1], ', '.join(MENSEN.keys()))
        sys.exit(1)

    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<!DOCTYPE mensa SYSTEM "http://student.hpi.uni-potsdam.de/openMensa.dtd">'

    code, html = get(uri=MENSEN[mensa])
    print '<mensa>'

    for meal in extract(html):
        print '  <!-- Mensa %s -->' % mensa
        print '  <meal name="%(name)s" date="%(date)s" category="%(category)s">' % meal
        print '    <description>%(description)s</description>' % meal
        print '  </meal>'

    print '</mensa>'
