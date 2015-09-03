#!/usr/bin/env python
# -*-coding:utf-8 -*

import argparse
from lib.scrapper import TheTVDB
from lib.mkvtags import BuildTag

# TODO gerer multilangue (ATTENTION mvk 3 lettres, TheTVDB : 2 lettres)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create mkv tag files from TheTVDB for series.')
    parser.add_argument('-p', '--path', help='Path to output directory', default='.')
    parser.add_argument('--id', help="""The TVDB identifier of the serie return by 'http://thetvdb.com/api/GetSeries.php?seriesname=<name>&language=<lang>'.""", required=True)

    args = parser.parse_args()

    serie, seasons, episodes = TheTVDB.getSerieInfos(args.id)

    tagbuilder = BuildTag(args.path)
    tagbuilder.serie(serie, seasons, episodes)
