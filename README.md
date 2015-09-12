# Video converter

Convert video to h265 with constant quality and add mkv metadata and poster.

## Requirements

* Handbrake
* mvkmerge

### Install requirements on debian like system

* ``apt-get install ``

## Install

* ``git clone https://github.com/aminotti/converter.git``
* ``pip install -r requirements.txt``

## Stage 1 : Build mkv tags file and attachments

Library to build kvm globals tags file.

Find id (series on http://thetvdb.com and movies on https://www.themoviedb.org) then run :

```bash
cd converter
./main.py -id <idmovie or idserie> [--film] -p </path/to/output/dir/>
```

## Stage 2 : user Handbrake and mkvmerge to build video file

### TODO
