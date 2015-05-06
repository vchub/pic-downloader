# NOTE: both works
# -*- coding: utf-8 -*-
# coding=utf-8

# multi-threading/processing base on article:
# http://chriskiehl.com/article/parallelism-in-one-line/

import csv
import unittest
import requests
import logging
# import threading
# import Queue

# Dummy is an exact clone of the multiprocessing module. The only difference is that, whereas multiprocessing works with processes, the dummy module uses threads (which come with all the usual Python limitations). So anything that applies to one, applies to the other. It makes it extremely easy to hop back and forth between the two. Which is especially great for exploratory programming when you’re not quite sure if some framework call is IO or CPU bound.
from multiprocessing.dummy import Pool as ThreadPool

import itertools

def transform_url(url):
    """create url of cloudinary transormation from url of uploaded picture
    create name of file to be saved

    :url: string
    :returns: (url: string, file_name:str, err: string)

    """
    url_arr = url.split('/')
    if len(url_arr) < 2 and url_arr[1] != '':
        logging.warning('not url: %s', url)
        return ( None, None, 'not url' )
    # res_arr = url_arr[:-1] + ['c_fit,h_570,q_80,r_0,w_380'] + url_arr[-1:]
    # return ('/'.join(res_arr), url_arr[-1], None)
    return (url, url_arr[-1], None)


def url_generator(csv_file):
    """yield url of transormation from csv_file

    :csv_file: string
    :yield: string

    """
    with open(csv_file, 'rb') as source:
        reader = csv.reader(source)
        # skip the 1st line
        reader.next()
        for row in reader:
            url = row[0]
            # don't yield not urls
            if not url:
                continue
            yield url


def file_downloawder(url, path = '../pics/'):
    """download file w/ url and write it path/file_name
    all Exception are logged, not raised

    :url: string
    :path: string
    :returns: (file_name, err)

    """
    try:
        pict_url, file_name, err = transform_url(url)
        if err:
            logging.error(err.message)
            return(None, err)
        with open(path + file_name, 'wb') as fd:
            r = requests.get(pict_url, stream=True)
            if r.status_code == 200:
                for chunk in r.iter_content(1024):
                    fd.write(chunk)
                logging.warning('file: %s done', file_name)
                return (file_name, None)
            else:
                logging.warning('status code: %s, url: %s', r.status_code, url)
                return (None, r.status_code)

    except Exception, e:
        logging.error(e.message)
        # TODO: remove in production: you don't want to stop
        # batch download b/c of one file/url error
        raise e



def main(csv_file, path, threads_num):
    """download pics from csv_file in several threads

    :csv_file: file name
    :path: dir for pics to be written
    :threads_num: int
    :returns: (num or pics written to dir, err)

    """
    urls = ( x for x in url_generator(csv_file))
    # Make the Pool of workers
    pool = ThreadPool(threads_num)
    # Open the urls in their own threads
    # and return the results
    # results = pool.map(file_downloawder, itertools.izip(urls, itertools.repeat(path)))
    # results = pool.map(file_downloawder, (urls, itertools.repeat("../pics/")))
    results = pool.map(file_downloawder, urls)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()



class TestDownloader(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_generator(self):
        f_name = 't1.csv'
        got = [x for x in url_generator(f_name)]
        self.assertTrue(len(got)==1)
        # print got
        # self.assertFalse(len(got) == 0)

    # @unittest.skip("return back")
    def test_file_downloader(self):
        f_name = 't2.csv'
        urls = ( x for x in url_generator(f_name))
        for url in urls:
            # write file to current dir
            # print 'url: ', url
            file_downloawder(url, '../pics/')

    def test_transform_url(self):
        url = 'http://res.cloudinary.com/dfqf1txhb/image/upload/v1411206268/xgi2icczxzwsjf1jxdpn.png'
        got = transform_url(url)
        self.assertIsNone(got[2])
        self.assertEqual(got[0].split('/')[1],'')
        # print got

    @unittest.skip("return back")
    def test_runner(self):
        main(csv_file = 't20.csv', path = '../pics/', threads_num = 20)


if __name__ == '__main__':
    main(csv_file = 'pictures.csv', path = '../pics/', threads_num = 20)

