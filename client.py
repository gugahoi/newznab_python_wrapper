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
# http://newznab.readthedocs.org/en/latest/misc/api/
class wrapper:
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

    def useXML(self):
        self.json = False

    def useJSON(self):
        self.json = True

    def setPassword(self, password):
        self.password = password

    def setUsername(self, username):
        self.username = username

    def setApi(self, api):
        self.api = api

    def devMode(self, flag):
        self.dev = flag

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
        result = '{}'
        try:
            result = urllib2.urlopen(url).read()
        except Exception, e:
            raise e

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

    def search(self, term, group=None, limit=None, cat=None, attrs=None, extended=None, maxage=None, offset=None, delete=None):
        """
        group=xxxx  List of usenet groups to search delimited by ”,”
        limit=123   Upper limit for the number of items to be returned.
        cat=xxx     List of categories to search delimited by ”,”
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {'q': term}
        if limit:
            params['limit'] = limit

        if maxage:
            params['maxage'] = maxage

        if offset:
            params['offset'] = offset

        if delete:
            params['del'] = delete

        if extended:
            params['extended'] = extended

        if group:
            params['group'] = group

        if cat:
            params['cat'] = cat

        if attrs:
            params['attrs'] = attrs

        url = self.build_url('search', params)
        return self.query(url)
