#! /usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import sys
import urllib2


def main():
    try:
        headers = {'Authorization': 'Token {}'.format(sys.argv[2])}
    except IndexError:
        sys.stderr.write("usage: %s <language_code> <API_KEY>\n" % sys.argv[0])
        return 1

    url = "https://www.lingq.com/api/languages/%s/lingqs/" % sys.argv[1]
    try:
        request = urllib2.Request(url, headers=headers)
    except urllib2.URLError:
        sys.stderr.write("Error: Could not connecting to %s\n" % url)
        return 1

    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError:
        sys.stderr.write("Error: Incorrect language code (%s) "
                         "or API_KEY (%s)\n" %
                         (sys.argv[1], sys.argv[2]))
        return 1

    content = response.read()
    lingqs = json.loads(content)
    for l in lingqs:
        term = l['term'].strip(',.;:"\' \t')
        hint = '; '.join(h['text'] for h in l['hints'])
        sentence = l['fragment']
        try:
            splits = sentence.lower().split(term.lower())
            sentence = '%s{%s}%s' % (splits[0], term, splits[1])
        except IndexError:
            pass
        line = '\"%s\", \"%s\", \"%s\"' % (term, hint, sentence)
        print(line.encode('utf-8'))


if __name__ == "__main__":
    sys.exit(main())
