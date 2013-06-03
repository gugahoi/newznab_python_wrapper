# -*- coding: utf-8 -*-
# Copyright (c) 2013 Gustavo Hoirisch <gugahoi@gmail.com>
# Licensed under the MIT license.
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

######################################################################
# Newznab API Wrapper
######################################################################

class NewzNabAPI:
    """Newznab API Wrapper class"""

    def __init__(self, address, api, username=None, password=None, useSSL=False):
        if 'http' in address:
            address = address[7:]

        self.url = address
        self.api = api
        self.username = username
        self.password = password

    def build_url(self, method, params=None):
        parameters = ''
        for p, x in params:
            parameters += '&%s=%s' % (p, x)

        return '%s/api?t=%s%s' % (self.url, method, parameters)
