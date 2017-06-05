from projectv2.crawler import parse, parse_soup
import requests
import redis
import json
import xlwt
from bs4 import BeautifulSoup


# the purpose of this method is to parse the infobox information of a single person and return to the web page
def parsesingle(name):
    # call the infobox crawler and get the list
    result_list = parse(name)
    # check the result list in case it is null.
    if not result_list:
        no_result = dict()
        # if null, output proper message
        no_result[name] = name + " has no Infobox!!"
        return no_result
    else:
        print(result_list)
        return result_list


# the purpose of this method is to parse the infobox information of a single person and writing in an Excel
def parselist(name):
    # connect to the redis database
    redisdb = redis.Redis(host='localhost', port=6379, db=0)
    # get the number of the elements in database
    size = redisdb.llen('wikipedia:items')
    # create excel file
    base = xlwt.Workbook()
    # initial the counter
    i = 0
    # set sheet name
    s = base.add_sheet("list")
    # retrieve all the element in the database
    while i < size:
        # find the query list in the database as a dictionary
        url_list = redisdb.lindex('wikipedia:items', i).decode("UTF-8")
        list_dict = json.loads(url_list)
        # check whether the current list name is the query
        if list_dict["fromlist"] == name.capitalize() + ' - Wikipedia':
            print("list found")
            m = 0
            # begin to get all the urls of people on the list and send to the infobox crawler
            for url in list_dict['address']:
                m = m + 1
                print("parsing url")
                # get the page soup of the current url
                response = requests.get(url)
                html_doc = response.text
                soup = BeautifulSoup(html_doc, "html5lib")
                # send to infobox crawler and get the result dictionary
                itemdict = parse_soup(soup)
                # if the person has infobox, parse the infobox and save in the excel
                if itemdict:
                    # write attribute and content in the same row
                    for key in itemdict:
                        print("writing excel")
                        m = m + 1
                        s.write(m, 0, key)
                        s.write(m, 1, itemdict[key])
                else:
                    s.write(m, 0, url+" has no Infobox")
            return base
        else:
            # the current list is not the query, check the next list
            i = i +1
            print("finding list in redis"+str(i))
    else:
        # the query is not in the database
        return "No such list"
