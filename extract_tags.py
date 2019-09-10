from lxml import html
from os import chdir
from os import listdir
from os.path import isfile, join
import json
import sys


def extract(page):
    parsed_page = html.fromstring(page)
    rows = parsed_page.xpath('//table[@class="table table-striped"]')[0].getchildren()[1].getchildren()
    records = []
    for row in rows:
        cells = row.getchildren()
        verified_img_src = cells[3].getchildren()[0].iterlinks().next()[2]
        record = {
            "address": cells[0].getchildren()[0].text,
            "tag": cells[1].getchildren()[0].text,
            "url": cells[2].getchildren()[0].text,
            "is_verified": True if "green" in (verified_img_src).lower() else False
        } 
        records.append(record)
    return records

def main(path):
    chdir(path)
    html_files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.html')]
    records = []
    for file_name in html_files:
        with open(file_name) as file_handler:
            page = file_handler.read()
            records += extract(page)
    tags = {}
    for record in records:
        address = record["address"]
        if address not in tags:
            tags[address] = {
                "tag": record["tag"],
                "url": record["url"],
                "is_verified": record["is_verified"]
            }
        else:
            if tags[address]["tag"] != record["tag"]:
                print("Tag conflict for address %s" % address)
    with open('blockchain_info_tags.json', 'wb') as file_handler:
        file_handler.write(json.dumps(tags))
    print 'Tags written to "{0}/blockchain_info_tags.json"...'.format(path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print '>> ERROR: Missing command line arguments!'
        print '\tUsage: python extract_tags.py [data_path]'
        print '\tExample: python extract_tags.py datasets/blockchain_info/submitted_links'
        sys.exit(1)
    main(sys.argv[1])
