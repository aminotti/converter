# Video converter

Convert video to h265 with constant quality and add mkv metadata and poster.

## Requirement

* Handbrake
* mvkmerge

### Install for debian like system

* ``apt-get install ``

## Library to build kvm globals tags file.

Search series ID with :

``http://thetvdb.com/api/GetSeries.php?seriesname=name&language=en``

```python
#!/usr/bin/env python
# -*-coding:utf-8 -*

from lib.scrapper import TheTVDB


if __name__ == '__main__':
    serie, seasons, episodes = TheTVDB.getSerieInfos('257655')
    print serie
    print seasons
    print episodes
```

TODO : convert python data to XML file for mkv tags file
