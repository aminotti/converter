#!/usr/bin/env python
# -*-coding:utf-8 -*

import argparse
from lib.scrapper import TheTVDB, TheMDB
from lib.mkvtags import BuildTag

# TODO gerer multilangue (ATTENTION mvk 3 lettres, TheTVDB : 2 lettres)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create mkv tag files for series and movies.')
    parser.add_argument('--id', help="""The TVDB or The moviedb identifier of the serie or film.""", required=True)
    parser.add_argument('--film', action="store_true", help='Request for movie tag instead of series tags.')
    parser.add_argument('-p', '--path', help='Path to output directory', default='.')

    args = parser.parse_args()

    if args.film:
        film = TheMDB.getFilmInfo(args.id)
        tagbuilder = BuildTag(args.path)
        tagbuilder.film(film)
    else:
        serie, seasons, episodes = TheTVDB.getSerieInfos(args.id)
        tagbuilder = BuildTag(args.path)
        tagbuilder.serie(serie, seasons, episodes)
