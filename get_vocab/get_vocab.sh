#!/bin/sh
curl -s "https://www.lingq.com/api/languages/$1/lingqs/" -H "Authorization: Token $2" > out

python << EOL

#!/usr/bin/env python
# -*- coding: utf-8 -*-    
import json, sys

def main():
	with open('out') as f:
		content = f.read()

	lingqs = json.loads(content)
	for l in lingqs:
		term = l['term']
		hint = l['hints'][0]['text']

		print "%s,%s" % (term, hint)

if __name__ == "__main__":
	main()

EOL

rm out

