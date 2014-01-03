#!/usr/bin/env python
# -*- coding: utf-8 -*-    

# First argument - file name
# Second argument - your locale (en?)

import json
import sys

def main():
	with open(sys.argv[1]) as f:
		content = f.read()


	lingqs = json.loads(content)
	for l in lingqs:
		#{u'fragment': u'5 \u041c\u0418\u041d\u0423\u0422 \xa0\u041e \xa0\u041f\u041e\u041b\u0418\u0422\u0418\u041a\u0415 \u2026', u'status': 0, u'term': u'\u043c\u0438\u043d\u0443\u0442', u'id': 26474593, u'hints': [{u'locale': u'en', u'text': u'minute', u'popularity': 63, u'id': 335140}]}
		term = l['term']
		hint = l['hints'][0]['text']

		print "%s,%s" % (term, hint)

if __name__ == "__main__":
	main()

