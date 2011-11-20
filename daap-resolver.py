#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by Christophe "Tito" De Wolf <tito@webtito.be> twitter.com/tito1337
# Licensed under GPLv3 (http://www.gnu.org/licenses/gpl)
######################################################################

import sys
import re
from struct import unpack, pack
import simplejson as json
from daap import DAAPClient
import logging

###################################################################### config
DAAP_HOST = "10.0.73.1"
DAAP_PORT = "3689"

###################################################################### logger
# TODO : disable this when fully tested
logger = logging.getLogger('daap-resolver')
hdlr = logging.FileHandler('.daap-resolver.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logger.info('Started')


###################################################################### resolver
class DAAPresolver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = DAAPClient()
        self.client.connect(host, port)
        logger.info("Connected to %s:%s"%(host,port))
        self.session = self.client.login()

        databases = self.session.databases()
        for d in databases:
            if str(d.id) == str(self.session.library().id):
                self.database = d

        self.tracks = self.database.tracks()
        logger.info("Got %s tracks"%len(self.tracks))
        
    def fulltext(self, search):
        #TODO : more effective search maybe?
        words = search.split()
        pattern = '(%s)'%('|'.join(words))
        founds = []
        logger.info('Searching %s in %d tracks'%(search, len(self.tracks)))
        for t in self.tracks:
            if len(re.findall(pattern, "%s %s %s"%(t.artist, t.album, t.name))) == len(words):
                found = dict()
                found["artist"] = t.artist
                found["track"]  = t.name
                found["album"]  = t.album
                if isinstance(t.time, int)
                    found["duration"] = int(t.time/1000):
                found["url"]    = 'http://%s:%s/databases/%d/items/%d.mp3?session-id=%s'%(self.host, self.port, self.database.id, t.id, self.session.sessionid)
                found["score"] = 1
                #found["source"] = 'DAAP'
                founds.append(found)
        logger.info('Found %d tracks'%len(founds))
        return founds
        
    def artistandtrack(self, artist, track):
        #TODO : more effective search maybe?
        founds = []
        logger.info('Searching %s - %s in %d tracks'%(artist, track, len(self.tracks)))
        for t in self.tracks:
            if re.search("%s"%artist, "%s"%t.artist, re.IGNORECASE ) and re.search("%s"%track, "%s"%t.name, re.IGNORECASE ):
                found = dict()
                found["artist"] = t.artist
                found["track"]  = t.name
                found["album"]  = t.album
                if isinstance(t.time, int)
                    found["duration"] = int(t.time/1000):
                found["url"]    = 'http://%s:%s/databases/%d/items/%d.mp3?session-id=%s'%(self.host, self.port, self.database.id, t.id, self.session.sessionid)
                found["score"] = 1
                #found["source"] = 'DAAP'
                founds.append(found)
        logger.info('Found %d tracks'%len(founds))
        return founds


###################################################################### functions
def print_json(o):
    s = json.dumps(o)
    sys.stdout.write(pack('!L', len(s)))
    sys.stdout.write(s)
    sys.stdout.flush()

###################################################################### init playdar
settings = dict()
settings["_msgtype"] = "settings"
settings["name"] = "DAAP Resolver"
settings["targettime"] = 200 # millseconds
settings["weight"] = 98 # mp3tunes results should be chosen just under the local collection
print_json( settings )


##################################################################### main
resolver = DAAPresolver(DAAP_HOST, DAAP_PORT)
while 1:
    length = sys.stdin.read(4)
    length = unpack('!L', length)[0]
    if not length:
        break
    if length > 4096 or length < 0:
        break
    if length > 0:
        msg = sys.stdin.read(length)
        request = json.loads(msg)
        logger.debug('Got request : %s'%request)
        if request['_msgtype'] == 'rq':
            if 'fulltext' in request: # User query
                tracks = resolver.fulltext(request['fulltext'])
            else:
                tracks = resolver.artistandtrack(request['artist'], request['track'])
                
            if len(tracks) > 0:
                response = { 'qid':request['qid'], 'results':tracks, '_msgtype':'results' }
                logger.debug('Sent response : %s'%response)
                print_json(response)
