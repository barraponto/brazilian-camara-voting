#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import csv, codecs, cStringIO
from lxml import etree
from lxml.cssselect import CSSSelector
from unicodewriter import UnicodeDictWriter

if __name__ == '__main__':
    # Start our list
    votings = []
    # Get the XML data
    root = etree.fromstring(open('camara.xml', 'r').read())
    # Optionally, get the XML data from an url
    # root = etree.parse('http://domain.com/source.xml')

    for voting in CSSSelector('Votacao')(root):
        thisvoting = {
            'description': voting.get('ObjVotacao'),
            'date': voting.get('Data'),
        }
        for deputado in CSSSelector('Deputado')(voting):
            row = {'name': deputado.get('Nome'),
                    'party': deputado.get('Partido'),
                    'state': deputado.get('UF'),
                    'stance': deputado.get('Voto')}
            row.update(thisvoting)
            votings.append(row)

    with open('pitacosdeputados.csv', 'wb') as csvfile:
        writer = UnicodeDictWriter(csvfile, ['description', 'date', 'name', 'party', 'state', 'stance'])
        for row in votings:
            writer.writerow(row)
