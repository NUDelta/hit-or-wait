import urllib2, json
import math
from math import radians,cos,sin,asin,sqrt,atan
import webbrowser

import operator

USERNAME = "yongsung"
#GOOGLE API KEYS
DIRECTION_KEY = "AIzaSyDJ2CPAKT3og0BtmVhFJUO8cd6InnbROLE" #google direction
ROADS_KEY ="AIzaSyA9HzWAEObRUTCGDEvEj2apbwVs1IzuhGU" #google roads
MAP_URL = "https://www.google.com/maps/@"

segmentDict = {}

#need ordered list for road segment:
segmentList = []

# testList = ['Brummel Street', 'Custer Avenue', 'Sheridan Road', 'North McCormick Boulevard', 'Ridge Avenue']
testList = []
testList1 = ['Brummel Street', 'Custer Avenue', 'Mulford Street']
testList2 = ['Brummel Street', 'Custer Avenue', 'Hull Terrace', 'Oakton Street']
testList3 = ['Brummel Street', 'Custer Avenue', 'Austin Street', 'Sherman Avenue']
testList4 = ['Brummel Street', 'Custer Avenue', 'Austin Street', 'Sherman Avenue']
testList5 = ['Brummel Street', 'Custer Avenue', 'Hull Terrace', 'Sherman Avenue']
testList6 = ['Brummel Street', 'Custer Avenue', 'Austin Street', 'Sherman Avenue']
testList7 = ['Brummel Street', 'Custer Avenue', 'Mulford Street', 'Sherman Avenue']
testList8 = ['Brummel Street', 'Custer Avenue', 'Austin Street', 'Sherman Avenue']
testList9 = ['Brummel Street', 'Custer Avenue', 'Case Street', 'Sherman Avenue']

testRoadDict = {}

# get one runner's lat,lng pairs from runkeeper dataset that I scraped a while ago.
# def cleanData():
#     f_out = open('data3.out','w')
#     map_data = ""
#     with open('route/evanston.json') as data_file:
#         #json.LOAD for files
#         data = json.load(data_file)
#         for i in data:
#             json_data = json.loads(i)
#             for j in json_data:
#                 latlng = str(j["latitude"]) + ","+ str(j["longitude"]) + "\n"
#                 map_data += latlng
#             f_out.write(map_data)
#             f_out.close()
#             break

#TODO: get draw routes function

##### Similar approach to 'A Markov Model for Driver Turn Prediction. John Krumm. SAE2008' ######

def getRoadIntersection(currentLat, currentLng):
    url_str = "http://api.geonames.org/findNearestIntersectionOSMJSON?lat=%s&lng=%s&username=%s" % (currentLat,currentLng,USERNAME)
    url = urllib2.urlopen(url_str)
    html = url.read()
    json_data = json.loads(html)["intersection"]
    #distance in meters
    distance = float(json_data["distance"])*1000
    bearing1 = json_data["street1Bearing"]
    bearing2 = json_data["street1Bearing"]
    currentRoadName = json_data["street1"]
    intersectedRoadName = json_data["street2"]
    intersectionLat = float(json_data["lat"])
    intersectionLng = float(json_data["lng"])

    # print distance, currentRoadName, intersectedRoadName,intersectionLat,intersectionLng
    distanceToIntersection = distance
    # distanceToIntersection = haversine(currentLat, currentLng, intersectionLat, intersectionLng)
    # only check if distance to the intersection is less than 20 meters.
    if distanceToIntersection <= 20:
        # check the probability of next intersection
        print "distance to the intersection is " + str(distanceToIntersection) + " meters"
        currentRoadName = getRoadSegments(currentLat,currentLng)
        getNextRoadProb(currentRoadName, intersectedRoadName)
    else:
        print "it is " + str(distanceToIntersection) + " to the intersection. TOO FAR!! \n\n"

    # haversine(float(currentLat),float(currentLng),float(intersectionLat),float(intersectionLng))
    # calculateBearing(float(currentLat),float(currentLng),float(intersectionLat),float(intersectionLng))
    # calculateNewLatLng(currentLat,currentLng,90,0.05)

def getRoadSegments(lat,lng):
    # either use google maps roads API: https://developers.google.com/maps/documentation/roads/intro
    # or geonames to get nearest road from geocoordinate.

    url_str = "http://api.geonames.org/findNearbyStreetsOSMJSON?lat=%s&lng=%s&username=%s" % (lat,lng,USERNAME)
    url = urllib2.urlopen(url_str)
    html = url.read()
    streetSegment = json.loads(html)["streetSegment"][0]
    segmentName = streetSegment["name"]
    print "currently on the road: " + segmentName
    return segmentName

    # if segmentName in segmentDict:
    #     segmentDict[segmentName] += 1
    # else:
    #     segmentDict[segmentName] = 1

    # put roadsegments in the previous history
    # this should be moved to data pre-processing

    # if segmentName not in segmentList:
    #     segmentList.append(segmentName)
    # print segmentList

#TODO: loading previous history: should put this somewhere.
def loadPreviousHistory():
    testList.append(testList1)
    testList.append(testList2)
    testList.append(testList3)
    testList.append(testList4)
    testList.append(testList5)
    testList.append(testList6)
    testList.append(testList7)
    testList.append(testList8)
    testList.append(testList9)

# given a road segment and previous history
# output probability of turn taking
def getNextRoadProb(roadName, intersectedRoadName):
    currentRoad = roadName
    cnt = 0
    for listItem in testList:
        if currentRoad in listItem:
            currentRoadIndex = listItem.index(currentRoad)
            # skip if it is last road segment.
            if currentRoadIndex == len(listItem)-1:
                continue
            cnt += 1
            nextRoadName = listItem[currentRoadIndex+1]
            if nextRoadName in testRoadDict:
                testRoadDict[nextRoadName] += 1
            else:
                testRoadDict[nextRoadName] = 1

    # print testRoadDict
    for key, value in testRoadDict.iteritems():
    # do something with value
        testRoadDict[key] = float(value)/cnt

    maxPair = max(testRoadDict.iteritems(), key=operator.itemgetter(1))
    prob = maxPair[1]

    print str(prob) + " chances to turn at " + maxPair[0]

    # if the intersected Road is also in the previous history print out the probability
    print "intersected road: " + intersectedRoadName
    if intersectedRoadName in testRoadDict:
        print str(testRoadDict[intersectedRoadName]) + " chances to turn at " + intersectedRoadName + "\n\n"
    else:
        print "intersected road is not in the previous route history. \n\n"
    # return maxPair[0], maxPair[1], prob
    # you should return testRoadDict divided by

    # # build a histogram of which road segments were encountered immediately after, and then normalize to get a discrete probability distribution
    # def calculatePrevRoadHistory:
    #     # input: current road segment
    #     # output: probability distribution for next road segment & turn

##### these are utils
#TODO: move to other file
def haversine(lat1, lon1, lat2, lon2):
    diffLong = math.radians(lon2 - lon1)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - (math.sin(math.radians(lat1))
            * math.cos(math.radians(lat2)) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    # print d

    # return in meters
    return d*1000.0

def calculateBearing(lat1,lng1,lat2,lng2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    diffLong = math.radians(lng2 - lng2)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    print compass_bearing

def calculateNewLatLng(lat,lng,bearing,distance):
    R = 6371 # km
    d = distance
    lat1 = math.radians(lat) #Current lat point converted to radians
    lon1 = math.radians(lng) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print(lat2,lon2)
    '''
    find nearest street check
    '''
    url_str = "http://api.geonames.org/findNearbyStreetsJSON?lat=%s&lng=%s&username=%s" % (lat2,lon2,username)
    url = urllib2.urlopen(url_str)
    html = url.read()
    print html
    # url = map_url + str(lat2) + "," + str(lon2)
    # webbrowser.open(url)

def checkPossibleStreets(lat,lng):
    directions = {'east':90,'west':270, 'south':180, 'north':360}
    dist = 0.03
    for k,v in directions:
        print k
        calculateNewLatLng(lat,lng,v,dist)

def main():
    loadPreviousHistory()

    # lastLat, lastLng = 42.01, -87.67
    # currentLat, currentLng = 42.022768, -87.680428

    # distance = haversine(lastLat, lastLng, currentLat, currentLng)

    latlngPairs = open('testData.out','r').readlines()
    for i in latlngPairs:
        tmp = i.split(",")
        currentLat, currentLng = tmp[0].strip(), tmp[1].split("\r")[0].strip()
        # print currentLat, currentLng
        getRoadIntersection(currentLat,currentLng)

    # only check every 50 meters.
    # if distance > 50.0:
        # for the lat,lng pair, check the nearest intersection
        # if it is within a certain distance get road Segment
        # getRoadIntersection(currentLat,currentLng)

if __name__ == "__main__":
    main()
