#!/usr/bin/env python
# -*-coding:utf-8 -*

from lib.scrapper import TheTVDB
from lib.mkvtags import BuildTag

# TODO gerer multilangue (ATTENTION mvk 3 lettres, TheTVDB : 2 lettres)

if __name__ == '__main__':
    serie, seasons, episodes = TheTVDB.getSerieInfos('257655')

    tagbuilder = BuildTag()
    tagbuilder.serie(serie, seasons, episodes)
