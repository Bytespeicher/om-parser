#!/usr/local/bin/python2.7
# -*- encoding: utf-8 -*-
#
# A Studentenwerk Thüringen Mensa scraper, producing XML for openMensa.

import sys; reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime, timedelta

from requests import get
from bs4 import BeautifulSoup

MENSEN = {
    'Ernst-Abbe-Platz': 'jena_eabp',
    'Philosophenweg': 'jena_philweg',
    'Carl-Zeiss-Promenade': 'jena_czprom',

    # 'Weimar': 'weimar'
}


def extract(html, mensa='eabp', day=0):
    """Extract meals from HTML and yielding them as dictlike-object."""

    soup = BeautifulSoup(html)

    for i in range(5):
        query = soup.find('a', href=lambda link: link.endswith('#%s_tag_%i_essen_%i' % (mensa, day, i)))

        if query is None:
            raise StopIteration

        yield type('Meal', (object, ), {
            'name': query.h3.text.strip().replace('-', ''),
            'note': query.p.text.strip().replace('-', ''),
            'price': query.p.findNext().text.split()[1].replace(',', '.')
        })()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: %s MENSA' % sys.argv[0]
        sys.exit(1)

    try:
        mensa = [key for key in MENSEN if key.lower().startswith(sys.argv[1].lower())][0]
        abbr = MENSEN[mensa]
    except IndexError:
        print '%s is not available. Try %s' % (sys.argv[1], ', '.join(MENSEN.keys()))
        sys.exit(1)

    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<!DOCTYPE cafeteria SYSTEM "http://om.altimos.de/open-mensa-v1.dtd">'

    r = get('http://www.thueringen.my-mensa.de/essen.php?mensa=%s' % abbr, allow_redirects=False)
    print '<cafeteria version="1.0">'
    print '  <!-- Studentenwerk Jena, %s -->' % mensa
    
    for day in range(5):
        print '  <day date="%s">' % (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')

        for i, meal in enumerate(extract(r.content, abbr, day)):
            print '    <category name="Essen %i">' % (i+1)
            print '      <meal>'
            print '        <name>' + meal.name + '</name>'
            if meal.note:
                print '        <note>' + meal.note + '</note>'
            print '        <price>' + meal.price + '</price>'
            print '      </meal>'
            print '    </category>'
        print '  </day>'
    print '</cafeteria>'
