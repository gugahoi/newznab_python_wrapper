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
            address = address.split("://")[1]

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
            hdr = {'User-Agent': 'Mozilla/5.0'}
            r = urllib2.Request(url, headers=hdr)
            result = urllib2.urlopen(r).read()
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

    def search(self, **extras):
        """
        q=xxx       Search input (URL/UTF-8 encoded). Case insensitive.
        group=xxxx  List of usenet groups to search delimited by ”,”
        limit=123   Upper limit for the number of items to be returned.
        cat=xxx     List of categories to search delimited by ”,”
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {}
        for key, value in extras.iteritems():
            params[key] = value

        return self.query(self.build_url('search', params))

    def tv(self, **extras):
        """
        q=xxx       Search input (URL/UTF-8 encoded). Case insensitive.
        season=xxx  Season string, e.g S13 or 13 for the item being queried.
        ep=xxx      Episode string, e.g E13 or 13 for the item being queried.
        cat=xxx     List of categories to search delimited by ”,”
        rid=xxx     TVRage id of the item being queried.
        limit=123   Upper limit for the number of items to be returned, e.g. 123.
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {}
        for key, value in extras.iteritems():
            params[key] = value
            print '%s = %s' % (key, value)

        return self.query(self.build_url('tvsearch', params))

    def movie(self, **extras):
        """
        q=xxx       Search input (URL/UTF-8 encoded). Case insensitive.
        imdbid=xxxx IMDB id of the item being queried e.g. 0058935.
        genre=xxx   A genre string i.e. ‘Romance’ would match ‘(Comedy, Drama, Indie, Romance)’
        cat=xxx     List of categories to search delimited by ”,”
        limit=123   Upper limit for the number of items to be returned, e.g. 123.
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {}
        for key, value in extras.iteritems():
            params[key] = value
            print '%s = %s' % (key, value)

        return self.query(self.build_url('movie', params))

    def music(self, **extras):
        """
        album=xxxx  Album title (URL/UTF-8 encoded). Case insensitive.
        artist=xxxx Artist name (URL/UTF-8 encoded). Case insensitive.
        label=xxxx  Publisher/Label name (URL/UTF-8 encoded). Case insensitive.
        track=xxxx  Track name (URL/UTF-8 encoded). Case insensitive.
        year=xxxx   Four digit year of release.
        genre=xxx   A genre string i.e. ‘Romance’ would match ‘(Comedy, Drama, Indie, Romance)’
        cat=xxx     List of categories to search delimited by ”,”
        limit=123   Upper limit for the number of items to be returned, e.g. 123.
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {}
        for key, value in extras.iteritems():
            params[key] = value
            print '%s = %s' % (key, value)

        return self.query(self.build_url('music', params))

    def book(self, **extras):
        """
        title=xxxx  Book title (URL/UTF-8 encoded). Case insensitive.
        author=xxxx Author name (URL/UTF-8 encoded). Case insensitive.
        limit=123   Upper limit for the number of items to be returned, e.g. 123.
        attrs=xxx   List of requested extended attributes delimeted by ”,”
        extended=1  List all extended attributes (attrs ignored)
        del=1       Delete the item from a users cart on download.
        maxage=123  Only return results which were posted to usenet in the last x days.
        offset=50   The 0 based query offset defining which part of the response we want.
        """
        params = {}
        for key, value in extras.iteritems():
            params[key] = value
            print '%s = %s' % (key, value)

        return self.query(self.build_url('book', params))

    def details(self, id):
        """id=xxxx  The GUID of the item being queried."""
        return self.query(self.build_url('book', {"guid": id}))

    def getnfo(self, id, raw=False):
        """
        id=xxxx The GUID of the item being queried.
        raw=1   If provided returns just the nfo file without the rss container
        """
        params = {"guid": id}
        if raw:
            params['raw'] = "1"

        return self.query(self.build_url('getnfo', params))

    def getnzb(self, id, delete=False):
        """
        id=xxxx The GUID of the item being queried.
        del=1   If provided removes the nzb from the users cart (if present)
        """
        params = {"guid": id}
        if delete:
            params['del'] = "1"

        return self.query(self.build_url('get', params))

    def addToCart(self, id):
        """
        id=xxxx The GUID of the item being queried.
        """
        return self.query(self.build_url('cartadd', {"guid": id}))

    def delFromCart(self, id):
        """
        id=xxxx The GUID of the item being queried.
        """
        return self.query(self.build_url('cartdel', {"guid": id}))

    def comments(self, id):
        """
        id=xxxx The GUID of the item being queried.
        """
        return self.query(self.build_url('comments', {"guid": id}))

    def addComment(self, id, text):
        """
        id=xxxx The GUID of the item being queried.
        text=xxxx   The comment being added (URL/UTF-8 encoded).
        """
        return self.query(self.build_url('commentadd', {"guid": id, "text": text}))

    def user(self, username):
        """
        username=xxx    A valid username (URL/UTF-8 encoded).
        """
        return self.query(self.build_url('user', {"username": username}))
