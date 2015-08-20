from mutagen.easyid3 import EasyID3 as id3
import os
import glob
import operator

def printMP3sInDir():
    path = raw_input("Path to Search?: ")
    for path, dirs, files in os.walk(path):
        files.sort()
        for filename in files:
            if not filename.lower().endswith('.mp3'):
                continue
            fullFileName = os.path.join(path, filename)
            try:
                mp3File = id3(fullFileName)
                print mp3File
                print fullFileName
                raw_input()
            except Exception:
                rep.error(fullFileName)
            else:
                print "Success"

global knownArtists
knownArtists = {}

def charCount(c,s):
    '''
        Returns the number of occurences of char c in string s
        c: char to find
        s: string to search in
    '''
    return len(s) - len(s.replace(c,''))

def getArtistAndAlbum(filename):
    title = ''
    artist = ''
    if '-' in filename:
        pass


def searchDirectory():
    path = raw_input("Path to Search?: ")
    numMP3s = 0
    for path, dirs, files in os.walk(path):
        files.sort()
        for filename in files:
            if not filename.lower().endswith('.mp3'):
                continue
            numMP3s += 1
            fullFileName = os.path.join(path, filename)
            try:
                mp3File = id3(fullFileName)
                #print mp3File
                #print "found and read file...",fullFileName
                if mp3File is None:
                    print "No tags"
                if "artist" in mp3File:
                    currArtist = str(mp3File["artist"])[3:-2]
                    if currArtist in knownArtists:
                        knownArtists[currArtist] += 1
                    else:
                        knownArtists[currArtist] = 1                        
            except Exception,e:
                print e
            else:
                pass
    print "Found",numMP3s,"mp3 files"
    print "Found Artists:"
    artistArr = []
    for eachArtist in sorted(knownArtists.keys()):
        #print eachArtist + " : " + str(knownArtists[eachArtist])
        artistArr.append((eachArtist,knownArtists[eachArtist]))
    artistArr.sort(key=operator.itemgetter(1),reverse=True)
    for eachItem in artistArr:
        print eachItem


searchDirectory()