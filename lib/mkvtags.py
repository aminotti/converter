# -*-coding:utf-8 -*

from lxml import etree
import sys
import os

from lib.rfc3339 import Rfc3339


class BuildTag(object):

    def __init__(self, destination='.'):
        self.destination = destination

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
