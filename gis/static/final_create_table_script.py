
# import Python's built-in JSON library
import sys, urllib.request, json, http.client, urllib.parse

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, Error

# import the JSON library from psycopg2.extras
from psycopg2.extras import Json

# import psycopg2's 'json' using an alias
from psycopg2.extras import json as psycop_json

# from config import config

# import Python's 'sys' library
import sys

# import Python's 're' library
import re

# import Python's 'datetime' library
from datetime import datetime, timedelta, timezone

# table_name = "json_data_earthquake"




url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson";
response = urllib.request.urlopen(url)
json_data = response.read()
record_list = json.loads(json_data)
feature_list = record_list['features']

# api to parse article, return json_article
conn = http.client.HTTPConnection('api.mediastack.com')

params = urllib.parse.urlencode({
    'access_key': 'd5d38f4421d7a60568ce0f63c5d62442',
    'categories': 'science,general',
    'sort': 'published_desc',
    'keywords': 'earthquake',
    'limit': 100
    })

conn.request('GET', '/v1/news?{}'.format(params))

res = conn.getresponse()
# data = res.read(500)
# data = res.read().decode('utf-8')
# d = json.loads(data)
# print(d)

if res.status == 200:
    data = res.read().decode('utf-8')
    json_article = json.loads(data)
    article_list = json_article['data']
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_article, f, ensure_ascii=False, indent=4)
    # print(json_article)


# fun to check place_Quake in  place_article
def findPlaceINStr(str_place, str_descript):
    list_of_place = str_place.strip(',.?!').split()
    for place in list_of_place:
        if place[0].isupper() and place in str_descript:
            return True
    return False

# fun to check mag_Quake in  mag_article
def findMagINStr(intMag, str_descript):
    for x in range(10):
        intMag +=0.1
        # print(intMag)
        intMag = round(intMag, 1)
        if str(intMag) in str_descript:
            return True
    return False

# fun to check time_Quake in  time_article
def isNowInTimePeriod(quekeTime, publishTime):
    startTime = quekeTime - timedelta(hours=10)
    # print(startTime)
    endTime = quekeTime + timedelta(hours=10)
    # print(endTime)
    if startTime < endTime:
        # return publishTime >= startTime and publishTime <= endTime
        return startTime <= publishTime and publishTime <= endTime
    else:
        #Over midnight:
        return publishTime >= startTime or publishTime <= endTime

# should return "<class 'list'>"
print ("\nJSON records object type:", type(feature_list))
table_name_Quake = "my_gis_earthquake"
print ("\ntable name for JSON data:", table_name_Quake)
columns_Quake = 'geography, datetime, place, mag'

table_name_article = "my_gis_article"
print ("\ntable name for JSON data:", table_name_article)
columns_article = 'title, public_datetime, article_content, url, fk_earthquake_id_id'


valuesQuake_str = ""
valuesArt_str = ""
fk_earthquake_id = 1

if type(feature_list) == list:
    for i in feature_list:
        for a in article_list:
            valuesQuake_temp = []
            valuesArt_temp = []
            # find point geometry
            geo_str = "ST_GeomFromText('POINT({} {})', 4326)".format(str(i['geometry']['coordinates'][0]), str(i['geometry']['coordinates'][1]))
            # geo_str = ' "'" + "ST_GeomFromText('POINT( " + str(i['geometry']['coordinates'][0]) + " " + str(i['geometry']['coordinates'][1]) + " )', 4326)" + "'"
            # val = geo_str.replace('"', '')
            # valuesQuake_temp.append(geo_str)
            magQuake = i['properties']['mag']
            if magQuake is None:
                magQuake = 0
            # convert bigint time to str time in UTS format
            timestamp = datetime.utcfromtimestamp(i['properties']['time']/ 1e3)
            # timestamp = datetime.fromtimestamp(i['properties']['time']/ 1e3, timezone.utc)
            # timestamp = timestamp.isoformat()
            # valuesQuake_temp.append(timestamp)
            # valuesQuake_temp.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            place = re.sub('\'','`',(i['properties']['place']))
            # valuesQuake_temp.append(place)
            #print(valuesQuake_temp)
            # fk_earthquake_id +=1
            if float(magQuake) >= 4.0:
                desc = re.sub('\'','`',(a['description']))
                title = re.sub('\'','`',(a['title']))
                chekmag = round(magQuake)
                chekmag = findMagINStr(chekmag-1, desc)
                publicDate = (a['published_at'])
                publicDate_obj = datetime.strptime(publicDate, '%Y-%m-%dT%H:%M:%S+00:00')
                # print(publicDate_obj)
                # print(timestamp)
                chekdate = isNowInTimePeriod(timestamp, publicDate_obj)
                chekplace = findPlaceINStr(place, desc)
                # print(chekdate, chekplace, chekmag)
                if chekdate and chekplace and chekmag:
                    valuesArt_temp.append(title)
                    valuesArt_temp.append(publicDate)
                    valuesArt_temp.append('\'{}\''.format(desc))
                    valuesArt_temp.append(a['url'])
                    valuesArt_temp.append(fk_earthquake_id)
                    # put parenthesis around each record string
                    valuesArt_temp = tuple(valuesArt_temp)
                    valuesArt_str += str(valuesArt_temp) + ",\n"
                    valuesArt_str = valuesArt_str.replace('"', '')
                    print("Value add to str valuesArt_ ")
        fk_earthquake_id +=1
        valuesQuake_temp.append(geo_str)
        valuesQuake_temp.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        valuesQuake_temp.append(place)
        valuesQuake_temp.append(magQuake)
        # put parenthesis around each record string
        valuesQuake_temp = tuple(valuesQuake_temp)
        valuesQuake_str += str(valuesQuake_temp) + ",\n"
        valuesQuake_str = valuesQuake_str.replace('"', '')
    # remove the last comma and end SQL with a semicolon
    valuesQuake_str = "{};".format(valuesQuake_str[:-2])
    print(valuesQuake_str)
    valuesArt_str = "{};".format(valuesArt_str[:-2])
    print(valuesArt_str)



# concatenate the SQL string

sql_string_Quake = "TRUNCATE TABLE %s RESTART IDENTITY CASCADE; INSERT INTO %s (%s)\nVALUES  %s" % (
    table_name_Quake,
    table_name_Quake,
    columns_Quake,
    valuesQuake_str
)
print( "Quake_str create")

sql_string_Art = "TRUNCATE TABLE %s RESTART IDENTITY CASCADE; INSERT INTO %s (%s)\nVALUES  %s" % (
    table_name_article,
    table_name_article,
    columns_article,
    valuesArt_str
)
print( "Art_str create")

try:
    # declare a new PostgreSQL connection object
    conn = connect(
        dbname = "test_json",
        user = "geo_django",
        host="localhost",
        password = "1234509876K",
        # attempt to connect for 3 seconds then raise exception
        connect_timeout = 3
    )

    cur = conn.cursor()
    print ("\ncreated cursor object:", cur)

except (Exception, Error) as err:
    print ("\npsycopg2 connect error:", err)
    conn = None
    cur = None
# only attempt to execute SQL if cursor is valid
if cur != None:

    try:
        # execute valuesQuake_str
        cur.execute(sql_string_Quake)
        conn.commit()

        print ('\nfinished INSERT INTO earthquake table')

        # execute valuesArt_str
        cur.execute(sql_string_Art)
        conn.commit()

        print ('\nfinished INSERT INTO article table')

    except (Exception, Error) as error:
        print("\nexecute_sql() error:", error)
        conn.rollback()
    # close the cursor and connection
    cur.close()
    conn.close()
