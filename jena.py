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

    # Jena
    'Ernst-Abbe-Platz': 'jena/mensa-ernst-abbe-platz',
    'Philosophenweg': 'jena/mensa-philosophenweg',
    'Carl-Zeiss-Promenade': 'jena/mensa-carl-zeiss-promenade',
    'vegeTable': 'jena/vegetable',
    'Cafeteria Bibliothek (ThulB)': 'jena/cafeteria-bibliothek-thulb',

    # 'Weimar': 'weimar'
    'Mensa am Park': 'weimar/mensa-am-park',

    # Eisenach
    'Mensa am Wartenberg': 'eisenach/mensa-am-wartenberg-2',

    # Erfurt
    'Nordhäuser Straße': 'erfurt/mensa-nordhaeuser-strasse',
    'Altonaer Straße': 'erfurt/mensa-altonaer-strasse',

    # Gera
    'Studienakademie Gera': 'gera/mensa-berufsakademie-gera',

    # Ilmenau
    'Ehrenberg': 'ilmenau/mensa-ehrenberg',
    'NANOteria': 'ilmenau/cafeteria-nanoteria',
}


def extract(html, mensa='eabp', day=0):
    """Extract meals from HTML and yielding them as dictlike-object."""

    soup = BeautifulSoup(html)
    div = soup.find('div', id="day_%i" % (day+2))

    # hidden in there as triple -> (müll, name, price)
    td = div.table.find_all('td') if div.table else []

    for i in range(0, len(td), 3):
        yield type('Meal', (object, ), {
            'name': next(td[i+1].stripped_strings),
            'note': "",
            'price': td[i+2].text.strip().replace(',', '.').rstrip(' €')
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

    r = get('http://www.stw-thueringen.de/deutsch/mensen/einrichtungen/%s.html' % abbr)
    print '<cafeteria version="1.0">'
    print '  <!-- Studentenwerk Jena, %s -->' % mensa

    for day in range(5):
        print '  <day date="%s">' % (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')

        # for i, meal in enumerate(extract(open('philo-dump.html'), abbr, day)):
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
