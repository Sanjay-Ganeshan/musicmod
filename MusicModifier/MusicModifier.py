from mutagen.easyid3 import EasyID3 as id3
import os
import glob
import operator
import re

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

def compareLengths(s1,s2):
    s1l = len(str(s1))
    s2l = len(str(s2))
    if s1l>s2l:
        return (1,0)
    elif s2l>s1l:
        return (0,1)
    else:
        return (0,0)

def artistSearch(artist):
    global knownArtists
    artist = str(artist)
    if artist in knownArtists:
        return True,artist
    else:
        for eachKnownArtist in knownArtists:
            if eachKnownArtist in artist:
                return True,eachKnownArtist
    return False,None

def artistPoints(s):
    global knownArtists
    isKnown,artistName = artistSearch(s)
    if isKnown:
        return int((knownArtists[artistName] + 3) / 2),artistName
    else:
        return 0,""
def compareToArtistDict(s1,s2):
    s1a = artistPoints(s1)
    s2a = artistPoints(s2)
    if s1a[0] > s2a[0]:
        return ((s1a[0]-s2a[0],0),s1a[1],0)
    elif s2a[0] > s1a[0]:
        return ((0,s2a[0]-s1a[0]),s2a[1],1)
    else:
        return ((0,0),None,-1)

def spacePoints(s):
    s = str(s)
    numSpaces = s.count(' ')
    return int((numSpaces + 1) / 2)

def compareSpaces(s1,s2):
    s1s = spacePoints(s1)
    s2s = spacePoints(s2)
    if s1s > s2s:
        return (s1s-s2s,0)
    else:
        return (0,s2s-s1s)

def getArtistAndAlbum(filename):
    baseFilename = str(filename.replace(".mp3","").split("\\")[-1])
    #baseFilename = re.sub(r"\(.*\)", "", baseFilename)
    #baseFilename = re.sub(r"ft\..*", "", baseFilename)
    #baseFilename = re.sub(r"\sfeat\s.*", "", baseFilename)
    title = ''
    artist = ''
    pointDict = {}
    if '-' in baseFilename:
        parts = baseFilename.split('-')
        for i in range(len(parts)):
            '''
            parts[i] = re.sub(r"\(.*\)", "", parts[i])
            parts[i] = re.sub(r"\?", "", parts[i])
            parts[i] = re.sub(r"\[.*\]", "", parts[i])
            parts[i] = re.sub(r"ft\..*", "", parts[i])
            parts[i] = re.sub(r"\sfeat(\.|\s).*", "", parts[i])
            '''
            parts[i] = re.sub(r"\sfeat(\.|\s).*|ft\..*|\[.*\]|\?|\(.*\)|\sHD\s", "", parts[i])
            parts[i] = parts[i].replace("  "," ")
            parts[i] = str(parts[i]).strip()
        if len(parts) == 2:
            #probably artist - name or name - artist
            #reset points -- higher points = more likely to be title (therefore negative = artist)
            pointDict[parts[0]] = 0 #more likely to be artist - name
            pointDict[parts[1]] = 1

            #check if the artist is already known
            knownKudos,suggestedArtistName,suggestedNumber = compareToArtistDict(parts[0],parts[1])
            if not(suggestedArtistName is None):
                del pointDict[parts[suggestedNumber]]
                pointDict[suggestedArtistName] = 1
                parts[suggestedNumber] = suggestedArtistName
            pointDict[parts[0]] -= knownKudos[0]
            pointDict[parts[1]] -= knownKudos[1]
            print "Known Kudos (",knownKudos[1],",",knownKudos[0],")"

            #check lengths. The longer is probably the title
            lenKudos = compareLengths(parts[0],parts[1])
            pointDict[parts[0]] += lenKudos[0]
            pointDict[parts[1]] += lenKudos[1]
            print "Length Kudos",lenKudos
            

            #check which has more spaces
            spacesKudos = compareSpaces(parts[0],parts[1])
            pointDict[parts[0]] += spacesKudos[0]
            pointDict[parts[1]] += spacesKudos[1]
            print "Space Kudos",spacesKudos
            
            if pointDict[parts[0]] > pointDict[parts[1]]:
                return parts[1],parts[0]
            else:
                return parts[0],parts[1]
    return "artist","song" 

def populateKnownSongsFromDirectory():
    pass

def searchDirectory():
    path = raw_input("Path to Search?: ")
    origPath = path
    numMP3s = 0
    allMp3s = []
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
                allMp3s.append(fullFileName)
                if mp3File is None:
                    print "No tags"
                if "artist" in mp3File:
                    currArtist = str(mp3File["artist"])[3:-2]
                    if currArtist in knownArtists:
                        knownArtists[currArtist] += 1
                    else:
                        knownArtists[currArtist] = 1
            except IOError,e:
                pass                       
            except Exception,e:
                print "Exception:",e
            else:
                pass
    print "Found",numMP3s,"mp3 files"

    numRight = 0
    numTotal = 0
    shouldBreak = False
    path = origPath

    #Print Found artists
    print "Found Artists:"
    artistArr = []
    for eachArtist in sorted(knownArtists.keys()):
        #print eachArtist + " : " + str(knownArtists[eachArtist])
        artistArr.append((eachArtist,knownArtists[eachArtist]))
    artistArr.sort(key=operator.itemgetter(1),reverse=True)
    for eachItem in artistArr:
        print eachItem
    
    res = getArtistAndAlbum("C:\Users\sanjay\Music\Miku\[60fps Full]  Senbonzakura _One Thousand Cherry Trees_- Hatsune Miku  DIVA English Romaji.mp3")
    print "Guessing...Artist:",res[0],"  Song Title:",res[1]
    for filename in allMp3s:
        if not filename.lower().endswith('.mp3'):
            continue
        fullFileName = os.path.join(path, filename)
        try:
            res = getArtistAndAlbum(fullFileName)
            if res[0] != 'artist' and res[1] != 'song':
                print "File:",fullFileName
                print "Guessing...Artist:",res[0],"  Song Title:",res[1]
                ans = raw_input("Right? (Y/N/Exit)  -->  ")
                if ans == "Exit":
                    shouldBreak = True
                    break
                elif ans.upper() == "Y":
                    numRight += 1
                numTotal += 1

        except Exception,e:
            raise e
        else:
            pass

    if numTotal == 0:
        numTotal = 1
    print numRight,"Guessed Correctly.",numTotal,"In Total.",int(float(numRight)/numTotal * 100),"% correct."

def main():
    searchDirectory()

if __name__ == "__main__":
    main()