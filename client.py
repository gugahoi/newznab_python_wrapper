# -*- coding: utf-8 -*-
# Copyright (c) 2013 Gustavo Hoirisch <gugahoi@gmail.com>
import urllib2
from urllib import quote_plus
try:
    import json
except ImportError:
    import simplejson as json


#######################
# Newznab API Wrapper #
#######################
class nnapi:
    """Newznab API Wrapper class"""

    def __init__(self, address, api, username=None, password=None, useSSL=False, useJson=True, dev=False):
        if 'http' in address:
            address = address[7:]

        self.url = address
        self.api = api
        self.username = username
        self.password = password
        self.json = useJson
        self.dev = dev
        self.cached = False

    def build_url(self, method='caps', params={}):
        parameters = ''
        for p, v in params.iteritems():
            parameters += '&%s=%s' % (p, quote_plus(v))

        if self.json:
            parameters += '&o=json'

        url = 'http://%s/api?t=%s%s&apikey=%s' % (self.url, method, parameters, self.api)
        if self.dev:
            print url
        return url

    def query(self, url):
        result = urllib2.urlopen(url).read()
        if self.dev:
            print result
        if self.json:
            result = json.loads(result)

        return result

    def caps(self):
        if not self.cached:
            url = self.build_url()
            result = self.query(url)
            self.cached = result

        return self.cached

    def categories(self):
        return self.caps()['categories']

    def genres(self):
        return self.caps()['genres']

    def groups(self):
        return self.caps()['groups']

    def search(self, term):
        url = self.build_url('search', {'q': term})
        return self.query(url)
