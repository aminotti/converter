#!/usr/bin/env python
# -*-coding:utf-8 -*

from lib.scrapper import TheTVDB


if __name__ == '__main__':
    serie, seasons, episodes = TheTVDB.getSerieInfos('257655')
    print serie
    print seasons
    print episodes
