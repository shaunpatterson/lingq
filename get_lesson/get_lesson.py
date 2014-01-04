#! /usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import sys
from urllib2 import Request, URLError, HTTPError, urlopen
from urlparse import urlparse, urlunparse
from urllib import quote
from string import replace
import os


url_base = 'https://www.lingq.com/api/languages'
API_KEY = None
LANGUAGE = None
TOP_DIR = None


def usage():
    return """usage: %s <language_code> <lesson_id|all> <API_KEY>
The given lesson must have been recently opened.
lesson_id is found under "i" tab to the right when opening a lesson,\
 look for
Share URL: http://www.lingq.com/learn/es/store/lesson/xxxxx/guest/
if lesson_id=all then all recently opened lessons (30 pieces)\
 are fetched\n""" %\
        sys.argv[0]


def lingq_getter(url_tail):
    headers = {'Authorization': 'Token {}'.format(API_KEY)}
    url = "%s/%s" % (url_base, url_tail)
    #sys.stderr.write("url: %s\n" % url)
    try:
        request = Request(url, headers=headers)
    except URLError:
        sys.stderr.write("Error: Could not connecting to %s\n" % url)
        sys.exit(1)
    try:
        response = urlopen(request)
    except HTTPError:
        sys.stderr.write("Error: opening URL %s\n" % url)
        sys.exit(1)
    content = response.read()
    return json.loads(content)


def read_args(indices):
    try:
        if sys.argv[1] in ('-h', '--help'):
            sys.stderr.write(usage())
            sys.exit(0)
        return tuple([sys.argv[x] for x in indices])

    except IndexError:
        sys.stderr.write(usage())
        sys.exit(1)


def escape_url(url):
    parsed = list(urlparse(url))
    parsed[2] = quote(parsed[2])
    return urlunparse(parsed)


def fetch_lesson(lesson_id, lessons):
    lesson_id = str(lesson_id)
    lesson = lingq_getter('%s/lessons/%s/' % (LANGUAGE, lesson_id))
    lesson2 = [less for less in lessons
               if str(less['id']) == lesson_id][0]

    base_name = '__'.join([lesson_id, lesson2['title'].encode('utf-8')])
    #lesson_dir = os.path.join(TOP_DIR, base_name)
    lesson_dir = TOP_DIR
    #os.mkdir(lesson_dir)
    if len(lesson2['audio_url']) > 0:
        # You can also use the with statement:
        audio_path = os.path.join(lesson_dir,
                                  ''.join([base_name, '.mp3']))
        audio_url = escape_url(lesson2['audio_url'].encode('utf-8'))
        try:
            with open(audio_path, 'wb') as f:
                f.write(urlopen(audio_url).read())
        except HTTPError:
            sys.stderr.write("Error fetching %s\n" % audio_url)

    text = lesson['text']
    for s in ['<b>', '</b>', '<p>', '</p>', '<br>', '</br>']:
        text = replace(text, s, '')

    text_path = os.path.join(lesson_dir,
                             ''.join([base_name, '.txt']))
    with open(text_path, 'w') as f:
        f.write(text.encode('utf-8'))


def main():
    global API_KEY, LANGUAGE, TOP_DIR
    (LANGUAGE, lesson_id, API_KEY) = read_args([1, 2, 3])
    TOP_DIR = 'fetched_lessons'
    os.mkdir(TOP_DIR)
    lessons = lingq_getter('%s/lessons/' % LANGUAGE)
    #How to start each in their own thread ??
    if lesson_id == 'all':
        for lesson in lessons:
            fetch_lesson(lesson['id'], lessons)
    else:
        fetch_lesson(lesson_id, lessons)
    return 0

if __name__ == "__main__":
    sys.exit(main())
