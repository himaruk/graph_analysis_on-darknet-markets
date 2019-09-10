"""Crawls blockchain.info/tags for tagged bitcoin addresses."""

import datetime
import urllib2
import os
import time
import socket
import ssl
import sys


def fetch_profile(filter_index, user_index, log_handler):
    """Download the tags page at a given index."""
    url = 'https://blockchain.info/tags?filter={0}&offset={1}'.format(filter_index, user_index)
    try:
        response = urllib2.urlopen(url, timeout=20)
    except urllib2.HTTPError as e:
        print '\n\nThe server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        log_handler.write(str(user_index) + '\n')
        return None
    except urllib2.URLError as e:
        print '\n\nWe failed to reach a server.'
        print 'Reason: ', e.reason
        log_handler.write(str(user_index) + '\n')
        return None
    except socket.timeout as e:
        print '\n\nThe request to server timed out.'
        print 'Reason: ', e.reason
        log_handler.write(str(user_index) + '\n')
    except ssl.SSLError as e:
        print '\n\nThe secure connection to server failed.'
        log_handler.write(str(user_index) + '\n')
    except e:
        print '\n\nGeneral error.'
        log_handler.write(str(user_index) + '\n')
    else:
        return response.read()


def crawl(start_index, end_index, filter_index, sleep_sec, log_handler):
    """Crawl all tags pages, with some delay."""
    error_count = 0
    for index in xrange(start_index, end_index+50, 50):
        page = fetch_profile(filter_index, index, log_handler)
        if sleep_sec > 0:
            time.sleep(sleep_sec)
        if not page:
            error_count += 1
            continue
        with open(str(index) + '.html', 'wb') as file_handler:
            file_handler.write(page)
        if (index + 1) % 10 == 0:
            print '\n\n[{0}] {1}/{2} pages crawled.'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                (index - start_index + 1),
                (end_index - start_index + 1))


def main(data_path, filter_index, start_index, end_index, sleep_sec):
    """Main entry point."""
    with open('{0}_{1}-{2}_error.log'.format(filter_index, start_index, end_index), 'wb') as log_handler:
        os.chdir(data_path)
        crawl(start_index, end_index, filter_index, sleep_sec, log_handler)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print '>> ERROR: Missing command line arguments!'
        print '\tUsage: python crawl_tags.py [data_path] [filter_index] [page_start_index] [page_end_index] [sleep_sec]'
        print '\n\tExample: python crawl_tags.py ~/projects/btc-mmm/datasets/blockchain_info 8 0 3550 2\n'
        print '\t\t   Page'
        print '\tFilter\tMin\tMax\tDescription:'
        print '\t2\t0\t2500\tBitcoinTalk profiles' 
        print '\t4\t0\t4650\tBitcoin-OTC profiles'  
        print '\t8\t0\t3550\tSubmitted links'
        print '\t16\t0\t26450\tSigned messages' 
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
