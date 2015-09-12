# -*-coding:utf-8 -*

import os
import requests
import StringIO
import zipfile
import tempfile
import shutil
from lxml import etree

from ..rfc3339 import Rfc3339


class TheTVDB(object):
    _key = '1D62F2F90030C444'

    @classmethod
    def _parseEpisodes(cls, dirname, filename):
        path = os.path.join(dirname, filename)
        serie = dict()
        seasons = dict()
        episodes = list()

        # Serie
        e = etree.parse(path)
        s = e.find('Series')
        serie['id'] = s.findtext('id')
        serie['poster'] = 'http://thetvdb.com/banners/' + s.findtext('poster')
        serie['release'] = Rfc3339.parse(s.findtext('FirstAired'))
        genre = s.findtext('Genre')
        if genre:
            serie['genre'] = genre.split('|')
            if genre.startswith('|'):
                del serie['genre'][0]
            if genre.endswith('|'):
                serie['genre'].pop()
        else:
            serie['genre'] = list()
        serie['name'] = s.findtext('SeriesName')
        serie['overview'] = s.findtext('Overview')
        rating = s.findtext('Rating')
        if rating:
            serie['rating'] = float(rating)
        else:
            serie['rating'] = 0
        serie['actors'] = cls._parseDistrib(os.path.join(dirname, 'actors.xml'))

        # Episodes
        seasonsid = None
        for episode in e.findall('Episode'):
            ep = dict()
            ep['id'] = episode.findtext('id')
            ep['season'] = episode.findtext('SeasonNumber')
            ep['seasonid'] = episode.findtext('seasonid')
            ep['episode'] = episode.findtext('EpisodeNumber')
            ep['title'] = episode.findtext('EpisodeName')
            ep['director'] = episode.findtext('Director')
            ep['overview'] = episode.findtext('Overview')
            ep['release'] = Rfc3339.parse(episode.findtext('FirstAired'))
            guest = episode.findtext('GuestStars')
            if guest:
                ep['guests'] = guest.split('|')
                if guest.startswith('|'):
                    del ep['guests'][0]
                if guest.endswith('|'):
                    ep['guests'].pop()
            else:
                ep['guests'] = list()
            rating = episode.findtext('Rating')
            if rating:
                ep['rating'] = float(rating)
            else:
                ep['rating'] = 0
            episodes.append(ep)

            # Seasons
            if seasonsid != ep['seasonid']:
                if type(ep['release']) is not str:
                    ep['release'] = ep['release'].year
                seasons[ep['seasonid']] = {'id': ep['seasonid'], 'year': ep['release'], 'number': ep['season'], 'episodes': 0}
                seasonsid = ep['seasonid']
            seasons[ep['seasonid']]['episodes'] = seasons[ep['seasonid']]['episodes'] + 1

        return serie, seasons, episodes

    @classmethod
    def _parseDistrib(cls, path):
        e = etree.parse(path)
        actors = list()
        for actor in e.findall('Actor'):
            a = dict()
            a['id'] = actor.findtext('id')
            a['name'] = actor.findtext('Name')
            a['role'] = actor.findtext('Role')
            a['poster'] = 'http://thetvdb.com/banners/' + actor.findtext('Image')
            actors.append(a)
        return actors

    @classmethod
    def getSerieInfos(cls, idserie, lang='fr'):
        url = 'http://thetvdb.com/api/{}/series/{}/all/{}.zip'.format(cls._key, idserie, lang)

        # Download and extract archive
        r = requests.get(url)
        if r.ok:
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            tmpdir = tempfile.mkdtemp()
            z.extractall(tmpdir)
            data = cls._parseEpisodes(tmpdir, '{}.xml'.format(lang))
            shutil.rmtree(tmpdir)
            return data
        else:
            print >> sys.stderr, "Erreur lors de la récupération de l'archive"
            return None, None, None
