#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as chrome_Options
from selenium.webdriver.firefox.options import Options as firefox_Options
from selenium.webdriver.opera.options import Options as opera_Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import psycopg2
#from psycopg2 import sql
#import psycopg2.extras
from psycopg2 import extras
from psycopg2.extras import NamedTupleConnection
#from psycopg2.extras import execute_values

from collections import namedtuple
from typing import (
  Dict
, List
, Tuple
, Set
 # Optional[X] is equivalent to Union[X, None]
, Optional
# an alternative to collections.namedtuple 
# that supports type-checking.
, NamedTuple 
# or 
#?#, SimpleNamespace
, Type 
# Callable[[int], str] is a function of (int) -> str.
, Callable
)
import argparse
import logging
from urllib import request as Request
from urllib.request import urlopen as URL_Open
import json
#
#
"""location_rating.py:
"""
__author__ = "GlukAlex"

steps = """
[from](https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=en)
Enter coordinates to find a place
On your computer, open Google Maps.
In the search box at the top, type your coordinates. Here are examples of formats that work:
* Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
* Degrees and decimal minutes (DMM): 41 24.2028, 2 10.4418
* Decimal degrees (DD): 41.40338, 2.17403
You'll see a pin show up at your coordinates.

Tips for formatting your coordinates
Here are some tips for formatting your coordinates so they work on Google Maps:
===
* Use the degree symbol instead of "d".
* Use periods as decimals, not commas. 
  * Incorrect: 41,40338, 2,17403. 
  * Correct: 41.40338, 2.17403. 
* List your latitude coordinates before longitude coordinates.
* Check that the first number in your latitude coordinate is between -90 and 90.
* Check that the first number in your longitude coordinate is between -180 and 180.

https://www.google.com/maps/place/59°26'02.4"N+24°44'24.0"E/@59.434,24.7378113,17z
                                                                               ^
                                                                               zoom level
Find and share places 
using plus codes
===
Plus codes work just like street addresses. 
When an address isn’t available, 
you can use a plus code 
to find or share a place on Google Maps, 
like your home or business.

A plus code includes:

6 or 7 letters and numbers
A town or city

Here’s an example of a plus code: 
X4HM+3C, Cairo, Egypt.  
                                                                             
# will return: 'CPMR+H2 Tallinn, Estonia'
from 
<span jstcache="275" 
  class="widget-pane-link" jsan="7.widget-pane-link">
  CPMQ+H4 Tallinn, Estonia</span> 
selector:  
$('span.widget-pane-link')  

# it works with redirect 
https://www.google.com/maps/place/59.434,24.7378113 

https://www.tripadvisor.com/
in 
//*[@id="taplc_trip_search_home_default_0"]/div[2]/div[1]/div/span/input
#taplc_trip_search_home_default_0 > div.ui_columns.datepicker_box.trip_search.metaDatePicker.rounded_lockup.easyClear.usePickerTypeIcons.hasDates > div.prw_rup.prw_search_typeahead.ui_column.is-3.responsive_inline_priority.search_typeahead.wctx-tripsearch > div > span > input
type: <location> | 'CPMR+H2 Tallinn, Estonia' + " " or "," + <restaurant name> | "Hilton"
then:
xPath: //*[@id="SUBMIT_HOTELS"]
css: #SUBMIT_HOTELS
redirect to: 
https://www.tripadvisor.com/Hotel_Review-g274958-d290521-Reviews-Hilton_Tallinn_Park-Tallinn_Harju_County.html
Where rating is in:
//*[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[1]/div/a/div/span
#taplc_resp_hr_atf_hotel_info_0 > div > div.ui_column.is-12-tablet.is-10-mobile.hotelDescription > div > a > div > span
<span class="ui_bubble_rating bubble_45" style="font-size:16px;" 
  alt="4.5 of 5 bubbles">
  </span>

[from](https://support.google.com/maps/answer/4610185?hl=en&ref_topic=3092444)
Find places in a specific area
To find places near an area you’ve searched for, follow the steps below.
===
* On your computer, open Google Maps.
* Search for a place.
* Press Enter or click Search .
* Click Nearby Search nearby.
* Type the kind of places you want to search, like hotels or airports.
* Press Enter or click Search . 
  You'll see search results 
  as red mini-pins and red dots, 
  where mini-pins show the top results. 
  The purple ones are ads. 
  Learn more about what the mini-pins mean.
* To go back to your original search result, 
  click the X Cancel Search nearby.

You can also use the term "near." 
For example, 
'coffee near central park' 
will return places to get coffee 
that are close to the park.

# to look at | output JSON file prettified content 
$ python -m json.tool toDo.json

# dependencies:
#$ pipenv shell

# syntax check 
#$ pyflakes location_rating.py

"""

def getMovieTitles( substr: str ) -> List[ str ]:
  """
  """
  # https://jsonmock.hackerrank.com/api/movies/search/?Title=spiderman
  url = """https://jsonmock.hackerrank.com/api/movies/search/?Title={}""".format( substr )
  data = ""
  # http.client.HTTPResponse
  with URL_Open( url ) as response:
    #
    print( "response.status:", response.status )
    print( "response.reason:", response.reason )
    print( "response.msg:", response.msg )
    print( "response.getheaders():", response.getheaders() ) 
    #
    # :bytes	
    data = response.read()
    # :str	
    data_Str = str( object = data, encoding = 'utf-8', errors = 'strict')
    # AttributeError: 'HTTPResponse' object has no attribute 'readall'
    ##data = response.readall()
    print( data[:25] )    
    print( data_Str[:25] )    
    #
    # TypeError: the JSON object must be str, not 'bytes'              
    #obj_JSON = json.load( fp = response )
    obj_JSON = json.loads( s = data_Str )
    #
    if 'data' in obj_JSON:
      movies_Data = obj_JSON[ 'data' ]
      print( movies_Data )
      return sorted( [ movie[ 'Title' ] for movie in movies_Data ] )		
    else:
      print( "failed to extract 'data' field from `obj_JSON`" )
      return [ "failed to get movie's Titles from `HTTPResponse`" ]

def main(
  connection_Str: str = ""
):
  """
  """
  if connection_Str == "":
    # Define|initialize to default connection string
    user = os.getenv( 
      #key, 
      # { b'USER', b'LOGNAME' }
      "LOGNAME",
      default = None 
    )
    # DSN
    connection_Str = (
      (
        #"host='localhost' " + 
        "dbname={} user={}"# +
        #" password={}"
      ).format(
        user, user
        #, "indent"
      )
    )
  #
  # print the connection string we will use to connect
  print( f"Connecting to database\n\t>{connection_Str}" )

  # psycopg2.connect(dsn, cursor_factory=NamedTupleCursor)
  with psycopg2.connect( connection_Str ) as connection:
    
    connection\
      .set_session( autocommit = True )
    
    with connection.cursor(
      cursor_factory = (
        #psycopg2.extras.DictCursor 
        psycopg2.extras.NamedTupleCursor
      )
    ) as cursor:
      
      # if not present 
      # create a new table with a single column called "name"
      #cursor.execute("""CREATE TABLE tutorials (name char(40));""")

      query_Insert_Into = "INSERT INTO test (field) VALUES($1);"
      args_Tuple = ( ( 1, ), ) * items_Total_n
      cursor\
        .execute(
          "INSERT INTO mytable VALUES (%s, %s, %s);"
        , ( 10, 20, 30 )
        )

      # class psycopg2.sql.SQL(string)
      # class psycopg2.sql.Identifier(string)  
      # to generate dynamically SQL queries 
      # (for instance choosing dynamically a table name):   
      #cursor\
      #  .execute(
      #    SQL( "INSERT INTO {} VALUES (%s)").format( Identifier('numbers') )
      #  , ( 10, )
      #  )  

  return None 

### /// *** unit test *** /// ###
if __name__ == "__main__":    
  # to prevent module execution 
  # while | when used | loaded with import 
  # like in tests 

  FORMAT_STR = (
    '%(asctime)s[%(levelname)s]'
    '%(module)s/%(name)s at:%(lineno)d -> %(message)s' 
  )

  logging\
    .basicConfig(
      # enables logging for selenium ?
      level = logging.DEBUG
      # - %(name)s - %(levelname)s
    , format = FORMAT_STR
    )
  logger = logging\
    .getLogger(
      #'get_info'
      __name__
    )
  formatter = logging.Formatter( FORMAT_STR )
  fh = logging.FileHandler( 'run.log', mode = 'w' )

  fh.setLevel( logging.DEBUG )
  fh.setFormatter( formatter )
  logger.addHandler( fh )

  # The connection parameters can be specified as 
  # a `libpq connection string` 
  # using the dsn parameter:
  #  conn = psycopg2.connect("dbname=test user=postgres password=secret")
  # or using a set of keyword arguments:
  #  conn = psycopg2.connect(dbname="test", user="postgres", password="secret")
  # The basic connection parameters are:
  #  dbname – the database name (database is a deprecated alias)
  #  user – user name used to authenticate
  #  password – password used to authenticate
  #  host – database host address (defaults to UNIX socket if not provided)
  #  port – connection port number (defaults to 5432 if not provided)
  connection_Str = input( 
    (
      "Type Keyword/Value DB connection parameters as \n" + 
      "host='localhost' dbname='my_database' user='postgres' password='secret'\n" + 
      "(for some cases user='user_name' will be enough)\n" + 
      "or just hit `Enter` to use defaults (for current system user):" 
    )
  )
  
  #main( items_Total_n, connection_Str )

  parser = argparse\
    .ArgumentParser(
      description = "Extract | scrap cars data from url"
    )
  args = parser.parse_args()
  
  #parser.print_help()
  main( **args )