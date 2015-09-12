# -*-coding:utf-8 -*

import sys
import json
from urllib2 import Request, urlopen

from ..rfc3339 import Rfc3339


class TheMDB(object):
    _key = '57983e31fb435df4df77afb854740ea9'

    @classmethod
    def getFilmInfo(cls, movieid, lang='fr'):
        base_url = "https://api.themoviedb.org/3"
        url_config = "{}/configuration?api_key={}".format(base_url, cls._key)
        url_detail = "{}/movie/{}?api_key={}&language={}".format(base_url, movieid, cls._key, lang)
        url_credit = "{}/movie/{}/credits?api_key={}&language={}".format(base_url, movieid, cls._key, lang)

        infos = dict()
        headers = {
            'Accept': 'application/json'
        }

        # API Config info
        request = Request(url_config, headers=headers)
        response = urlopen(request)
        config = json.load(response)

        # Movie infos
        request = Request(url_detail, headers=headers)
        response = urlopen(request)
        data = json.load(response)
        infos['id'] = data['id']
        infos['imdb_id'] = data['imdb_id']
        infos['countries'] = list()
        for c in data['production_countries']:
            infos['countries'].append(c['iso_3166_1'])
        infos['revenue'] = data['revenue']
        infos['adult'] = data['adult']
        infos['release'] = Rfc3339.parse(data['release_date'])
        infos['vote'] = data['vote_average']
        infos['title'] = data['title']
        infos['original_title'] = data['original_title']
        if data['poster_path']:
            infos['cover'] = config['images']['secure_base_url'] + 'original' + data['poster_path']
        else:
            infos['cover'] = None
            print >> sys.stderr, "Pas d'affiche disponible"
        if data['backdrop_path']:
            infos['cover_land'] = config['images']['secure_base_url'] + 'original' + data['backdrop_path']
        else:
            infos['cover_land'] = None
            print >> sys.stderr, "Pas d'affiche paysage disponible"
        infos['genres'] = list()
        for g in data['genres']:
            infos['genres'].append(g['name'])
        infos['overview'] = data['overview']

        # Credits
        request = Request(url_credit, headers=headers)
        response = urlopen(request)
        data = json.load(response)
        infos['actors'] = list()
        for cast in data['cast']:
            a = dict()
            a['id'] = cast['id']
            a['name'] = cast['name']
            a['role'] = cast['character']
            if cast['profile_path']:
                a['poster'] = config['images']['secure_base_url'] + 'original' + cast['profile_path']
            else:
                a['poster'] = ''
            infos['actors'].append(a)

        infos['directors'] = list()
        infos['screenplay'] = list()
        infos['producers'] = list()
        for crew in data['crew']:
            if crew['job'] == 'Director':
                infos['directors'].append(crew['name'])
            elif crew['job'] == 'Producer':
                infos['producers'].append(crew['name'])
            elif crew['job'] == 'Screenplay':
                infos['screenplay'].append(crew['name'])

        return infos
