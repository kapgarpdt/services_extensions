#!/usr/bin/env python
import json
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

csvfile = "extensions_services.csv"
with open(csvfile, "a") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow( ['extension_name','extension_type', 'service_name'])
	

API_ACCESS_KEY=''
BASE_URL = 'https://api.pagerduty.com'
HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=API_ACCESS_KEY),
		'Content-type': 'application/json'
	}

	
def get_extensions():
	global extensions_count
	more = True
	all_extensions = requests.get(BASE_URL + '/extensions', headers=HEADERS)
	while more:
		for extension in all_extensions.json()['extensions']:
			for object in extension['extension_objects']:
				if object['type'] == 'service_reference':
					with open(csvfile, 'a') as output:
						writer = csv.writer(output, lineterminator='\n')
						row = [extension['name'], extension['extension_schema']['summary'], object['summary']]
						#print(row)
						writer.writerow(row)
		more = all_extensions.json()['more']
		offset = all_extensions.json()['offset'] + all_extensions.json()['limit']
		params = {
		'offset':offset
		}
		print(offset)
		all_extensions = requests.get(BASE_URL + '/extensions', headers=HEADERS, params=params)
		
	    	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	get_extensions()
	

if __name__=='__main__':
	sys.exit(main())
