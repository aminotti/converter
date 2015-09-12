# -*-coding:utf-8 -*

import sys
import os
from lxml import etree
import urllib

from lib.rfc3339 import Rfc3339


class BuildTag(object):

    def __init__(self, destination='.'):
        self.destination = destination

    def film(self, film, lang='fre'):
        tags = etree.XML('''<!DOCTYPE Tags SYSTEM "matroskatags.dtd"><Tags></Tags>''')
        tag = etree.SubElement(tags, "Tag")

        target = etree.SubElement(tag, "Targets")
        etree.SubElement(target, "TargetTypeValue").text = "50"
        etree.SubElement(target, "TargetType").text = "MOVIE"

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "RATING"
        etree.SubElement(simple, "String").text = str(film['vote'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TITLE"
        etree.SubElement(simple, "String").text = film['original_title']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "DATE_RELEASE"
        etree.SubElement(simple, "String").text = Rfc3339.reverse(film['release'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TMDbID"
        etree.SubElement(simple, "String").text = str(film['id'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "IMDBID"
        etree.SubElement(simple, "String").text = film['imdb_id']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "GENRE"
        film['genres'].sort()
        etree.SubElement(simple, "String").text = ", ".join(film['genres'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "DIRECTOR"
        film['directors'].sort()
        etree.SubElement(simple, "String").text = ", ".join(film['directors'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "PRODUCER"
        film['producers'].sort()
        etree.SubElement(simple, "String").text = ", ".join(film['producers'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "SCREENPLAY_BY"
        film['screenplay'].sort()
        etree.SubElement(simple, "String").text = ", ".join(film['screenplay'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "SUMMARY"
        etree.SubElement(simple, "TagLanguage").text = lang
        etree.SubElement(simple, "DefaultLanguage").text = str(1)
        etree.SubElement(simple, "String").text = film['overview']

        for actor in film['actors']:
            simple = etree.SubElement(tag, "Simple")
            etree.SubElement(simple, "Name").text = "ACTOR"
            etree.SubElement(simple, "String").text = actor['name']
            simple1 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple1, "Name").text = "TMDbID"
            etree.SubElement(simple1, "String").text = str(actor['id'])
            simple2 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple2, "Name").text = "CHARACTER"
            etree.SubElement(simple2, "String").text = actor['role']
            simple3 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple3, "Name").text = "URL"
            etree.SubElement(simple3, "String").text = actor['poster']

        root = etree.ElementTree(tags)
        # root.write(sys.stdout, pretty_print=True, xml_declaration=True, encoding="UTF8")
        filename = "{} ({}).xml".format(film['title'].encode('utf8'), film['release'].strftime('%Y'))
        filename = filename.replace("/", "-")
        root.write(os.path.join(self.destination, filename), pretty_print=True, xml_declaration=True, encoding="UTF8")
        if film['cover']:
            urllib.urlretrieve(film['cover'], os.path.join(self.destination, 'cover{}'.format(os.path.splitext(film['cover'])[1])))
        if film['cover_land']:
            urllib.urlretrieve(film['cover_land'], os.path.join(self.destination, 'cover_land{}'.format(os.path.splitext(film['cover_land'])[1])))

    def serie(self, serie, seasons, episodes, lang='fre'):
        for episode in episodes:
            Tags = etree.XML('''<!DOCTYPE Tags SYSTEM "matroskatags.dtd"><Tags></Tags>''')
            season = seasons[episode['seasonid']]

            serieTag = etree.SubElement(Tags, "Tag")
            self._buildSerie(serieTag, serie, lang)

            seasonTag = etree.SubElement(Tags, "Tag")
            self._buildSeason(seasonTag, season)

            episodeTag = etree.SubElement(Tags, "Tag")
            self._buildEpisode(episodeTag, episode, lang)

            root = etree.ElementTree(Tags)
            # root.write(sys.stdout, pretty_print=True, xml_declaration=True, encoding="UTF8")
            filename = "{}-S{}E{}-{}.xml".format(serie['name'].encode('utf8'), str(episode['season']).zfill(2), str(episode['episode']).zfill(2), episode['title'].encode('utf8'))
            filename = filename.replace("/", "-")
            root.write(os.path.join(self.destination, filename), pretty_print=True, xml_declaration=True, encoding="UTF8")

    def _buildSerie(self, tag, serie, lang):
        target = etree.SubElement(tag, "Targets")
        etree.SubElement(target, "TargetTypeValue").text = "70"
        etree.SubElement(target, "TargetType").text = "COLLECTION"

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "RATING"
        etree.SubElement(simple, "String").text = str(serie['rating'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TITLE"
        etree.SubElement(simple, "String").text = serie['name']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TheTVDBID"
        etree.SubElement(simple, "String").text = serie['id']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "GENRE"
        serie['genre'].sort()
        etree.SubElement(simple, "String").text = ", ".join(serie['genre'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "SUMMARY"
        etree.SubElement(simple, "TagLanguage").text = lang
        etree.SubElement(simple, "DefaultLanguage").text = str(1)
        etree.SubElement(simple, "String").text = serie['overview']

        for actor in serie['actors']:
            simple = etree.SubElement(tag, "Simple")
            etree.SubElement(simple, "Name").text = "ACTOR"
            etree.SubElement(simple, "String").text = actor['name']
            simple1 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple1, "Name").text = "TheTVDBID"
            etree.SubElement(simple1, "String").text = actor['id']
            simple2 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple2, "Name").text = "CHARACTER"
            etree.SubElement(simple2, "String").text = actor['role']
            simple3 = etree.SubElement(simple, "Simple")
            etree.SubElement(simple3, "Name").text = "URL"
            etree.SubElement(simple3, "String").text = actor['poster']

    def _buildSeason(self, tag, season):
        target = etree.SubElement(tag, "Targets")
        etree.SubElement(target, "TargetTypeValue").text = "60"
        etree.SubElement(target, "TargetType").text = "SEASON"

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TheTVDBID"
        etree.SubElement(simple, "String").text = season['id']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "PART_NUMBER"
        etree.SubElement(simple, "String").text = str(season['number'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "DATE_RELEASE"
        etree.SubElement(simple, "String").text = str(season['year'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TOTAL_PARTS"
        etree.SubElement(simple, "String").text = str(season['episodes'])

    def _buildEpisode(self, tag, episode, lang):
        target = etree.SubElement(tag, "Targets")
        etree.SubElement(target, "TargetTypeValue").text = "50"
        etree.SubElement(target, "TargetType").text = "EPISODE"

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TheTVDBID"
        etree.SubElement(simple, "String").text = episode['id']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "PART_NUMBER"
        etree.SubElement(simple, "String").text = episode['episode']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "DATE_RELEASE"
        etree.SubElement(simple, "String").text = Rfc3339.reverse(episode['release'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "RATING"
        etree.SubElement(simple, "String").text = str(episode['rating'])

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "TITLE"
        etree.SubElement(simple, "String").text = episode['title']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "DIRECTOR"
        etree.SubElement(simple, "String").text = episode['director']

        simple = etree.SubElement(tag, "Simple")
        etree.SubElement(simple, "Name").text = "SUMMARY"
        etree.SubElement(simple, "TagLanguage").text = lang
        etree.SubElement(simple, "DefaultLanguage").text = str(1)
        etree.SubElement(simple, "String").text = episode['overview']

        for guest in episode['guests']:
            simple = etree.SubElement(tag, "Simple")
            etree.SubElement(simple, "Name").text = "ACTOR"
            etree.SubElement(simple, "String").text = guest
