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
import os
import sys 
from pprint import pprint, pformat  
from contextlib import contextmanager  
from enum import Enum#, unique
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

for location search: 
you should try adding a zip, or try a larger nearby city.
e.g. near San Francisco, CA
Try adding a city, state, or zip code.

https://www.tripadvisor.com/
[API Description](https://developer-tripadvisor.com/content-api/description/)
Approved users of the TripAdvisor Content API 
can access the following business details 
for accommodations, restaurants, and attractions:  
* Location ID, name, address, latitude & longitude
* Read reviews link, write-a-review link
* Overall rating, ranking, subratings, 
  awards, the number of reviews the rating is based on, 
  rating bubbles image

document.forms[0].elements
0: input#mainSearch.text.focusClear
1: input#GEO_SCOPED_SEARCH_INPUT.text.geoScopeInput.focusClear
2: button#SEARCH_BUTTON.search_button
3: input#TYPEAHEAD_GEO_ID
4: input#TYPEAHEAD_LATITUDE
5: input#TYPEAHEAD_LONGITUDE
6: input#TYPEAHEAD_NEARBY
7: input
8: input#TOURISM_REDIRECT
9: input#MASTAHEAD_TYPEAHEAD_START_TIME
10: input#MASTAHEAD_TYPEAHEAD_UI_ORIGIN
11: input#MASTHEAD_MAIN_QUERY
12: input#MASTHEAD_SUPPORTED_SEARCH_TYPES
13: input#MASTHEAD_ENABLE_NEAR_PAGE
14: input
15: input
16: input#SOCIAL_TYPEAHEAD_2018_FEATURE
length: 17

TYPEAHEAD_GEO_ID: input#TYPEAHEAD_GEO_ID
TYPEAHEAD_LATITUDE: input#TYPEAHEAD_LATITUDE
TYPEAHEAD_LONGITUDE: input#TYPEAHEAD_LONGITUDE
TYPEAHEAD_NEARBY: input#TYPEAHEAD_NEARBY
enableNearPage: input#MASTHEAD_ENABLE_NEAR_PAGE
geo: input#TYPEAHEAD_GEO_ID
latitude: input#TYPEAHEAD_LATITUDE
  document.querySelector('input#TYPEAHEAD_LATITUDE').value = "59.434";
longitude: input#TYPEAHEAD_LONGITUDE
  document.querySelector('input#TYPEAHEAD_LONGITUDE').value = "24.7378113";
mainSearch: input#mainSearch.text.focusClear
pid: input
q: input#MASTHEAD_MAIN_QUERY
redirect: input#TOURISM_REDIRECT
returnTo: input
searchNearby: input#TYPEAHEAD_NEARBY

supportedSearchTypes: input#MASTHEAD_SUPPORTED_SEARCH_TYPES
<input id="MASTHEAD_SUPPORTED_SEARCH_TYPES" 
  type="hidden" name="supportedSearchTypes" 
  value="find_near_stand_alone_query">

in 
xPath: //*[@id="taplc_trip_search_home_default_0"]/div[2]/div[1]/div/span/input
css_Selector: #taplc_trip_search_home_default_0 > 
  div.ui_columns.datepicker_box.trip_search.metaDatePicker
  .rounded_lockup.easyClear.usePickerTypeIcons.hasDates > 
  div.prw_rup.prw_search_typeahead.ui_column.is-3
  .responsive_inline_priority.search_typeahead.wctx-tripsearch > 
  div > span > input
document.querySelector('input.typeahead_input');
document.querySelector('input.typeahead_input').value;
>"Hilton Tallinn Park, Tallinn, Estonia"

type: <location> | 'CPMR+H2 Tallinn, Estonia' + " " or "," + <restaurant name> | "Hilton"
?!?
document.getElementById("SEARCH_BUTTON");
<button id=​"SEARCH_BUTTON" class=​"search_button" 
  type=​"submit" 
  onclick= ... >​…​</button>​
!?!

then:
xPath: //*[@id="SUBMIT_HOTELS"]
css_Selector: #SUBMIT_HOTELS
document.getElementById("SUBMIT_HOTELS");
<button id="SUBMIT_HOTELS" class="form_submit" 
  onclick="(ta.prwidgets.getjs(this,'handlers')).run('/Hotels')" 
  tabindex="5">
    <span class="ui_icon search submit_icon"></span>
    <span class="submit_text">Find hotels</span>
</button>
document.getElementById("SUBMIT_HOTELS").click();

redirect to: 
https://www.tripadvisor.com/Hotel_Review-g274958-d290521-Reviews-Hilton_Tallinn_Park-Tallinn_Harju_County.html
Where rating is in:
//*[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[1]/div/a/div/span
#taplc_resp_hr_atf_hotel_info_0 > div > 
  div.ui_column.is-12-tablet.is-10-mobile.hotelDescription > div > a > div > span
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

Command line usage | useful commands:
===
# to look at | output JSON file prettified content 
$ python -m json.tool toDo.json

# dependencies:
#$ pipenv shell

# syntax check 
#$ pyflakes location_rating.py
# to discover and check all in current | root directory: 
#$ python3 -m pyflakes .
# to discover and check all in 'tests' directory: 
#$ python3 -m pyflakes tests
# to filter issues:
$ python3 -m pyflakes . | grep "undefined"

# run:
# to show help message and exit:
$ location_rating.py --help 
# or: 
$ location_rating.py -h  

"""

class Location_Rating( NamedTuple ):
    """ Represents a row | record 
    in 'locations_ratings' table . 

    location_Rating = Location_Rating( 
      latitude = "59.434", longitude = "24.7378113"
    , location = "CPMR+H2 Tallinn, Estonia"
    , restaurant_name = "Hilton"
    , rating = "4.5 of 5 bubbles"
    )
    """
    #from decimal import *
    # Decimal <=> numeric
    #>>> Decimal('3.14')
    #Decimal('3.14')
    #>>> Decimal((0, (3, 1, 4), -2))
    #Decimal('3.14')
    # NUMERIC( 8, 6 )
    latitude: str # char(10) NOT NULL, 
    longitude: str # char(10) NOT NULL, 
    location: str # text NOT NULL, 
    restaurant_name: str # text NOT NULL, 
    rating: str # text NOT NULL,
    #PRIMARY KEY( latitude, longitude )

class Driver_Option( NamedTuple ):
  """
  """
  driver: 'WebDriver' = webdriver.Chrome
  # keyargs 
  options: Dict[ str, 'Options' ] = { 'chrome_options': webdriver.ChromeOptions() } 

class NoValue(Enum):
  """
  """
  def __repr__(self):
    return f'<{self.__class__.__name__}.{self.name}>'

class Page_Load_Strategy( NoValue ):
  """
  """
  NONE = 'none'
  NORMAL = 'normal'
  EAGER = 'eager'

@contextmanager
def web_Driver_Context(
  implicit_Wait: int = 0 # second(s)
#?#, wait_Delay: int = 3 # second(s)
, headless: bool = True
#, driver_i: int = 0  
, driver_Name: str = "chrome"
#, page_Load_Strategy: str = "none"
, page_Load_Strategy: Page_Load_Strategy = Page_Load_Strategy.NONE
):
  """
  """
  desired_Capabilities_Dic = { 
    'pageLoadStrategy': page_Load_Strategy.value#[ "none", "normal", 'eager'][0] 
  }
  driver_Config_Map = {
    'chrome': Driver_Option( 
        driver = webdriver.Chrome
      , options = { 
          # DeprecationWarning: use options instead of chrome_options
          #?#'chrome_options'
          'options': webdriver.ChromeOptions()
        } 
      )
  }
  ( 
    driver_Factory
  , driver_Options 
  ) = driver_Config_Map.get( driver_Name )
  driver = None

  # acquire resource:
  try:
    # This iterator must yield exactly one value, 
    # which will be bound 
    # to the targets 
    # in the 'with' statement’s 'as' clause, 
    # if any.

    #if headless:
      #options
    # DeprecationWarning: use setter for headless property instead of set_headless  
    #>print( "dir( driver_Options[ 'options' ] ):", dir( driver_Options[ "options" ] ) )
    #tuple( driver_Options
    #  .values() )[0]\
    driver_Options[ "options" ].headless = headless 
      # Options -> self.headless = headless 
      # class property(fget=None, fset=None, fdel=None, doc=None)
      # @headless.setter
      #?#.set_headless( headless = headless )
      # 'Options' object has no attribute 'setter' 
      #!#.setter( headless = headless ) 

    # driver = webdriver.Firefox( firefox_options = options )
    driver = driver_Factory( 
        desired_capabilities = desired_Capabilities_Dic 
      , **driver_Options 
      )

    if implicit_Wait > 0:

      driver.implicitly_wait( implicit_Wait )

    yield driver
  finally:
    # release resource: 
    if driver is not None:  
      driver.quit() 

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

def get_Connection_DSN() -> str:
  """
  """
  #DSN = 'dbname=test_db'

  # environ['HOME'] 
  # os.getlogin() 
  # getpass.getuser()
  #   Return the “login name” of the user.
  # This function checks the environment variables 
  # LOGNAME, USER, LNAME and USERNAME, in order, 
  # and returns the value 
  # of the first one 
  # which is set to a non-empty string. 
  # If none are set, 
  # the login name from the password database is returned 
  # on systems which support the 'pwd' module, 
  # otherwise, an exception is raised.
  # In general, 
  # this function should be preferred over os.getlogin().
  if 1 == 0:
    DSN = os.getenv( 
        "PostgreSQL_Dev_DSN"
      , default = 'dbname=test_db' 
      )

  DSN = os.getenv( 
      "PostgreSQL_Dev_DSN"
    , default = None 
    )

  if DSN is None:
  
    DSN = 'dbname=test_db'
    os.environ[ 'PostgreSQL_Dev_DSN' ] = DSN  

  return DSN

def create_Table(
  #connection_Str: str = "dbname=test_db"
  connection#: psycopg2.extensions.connection
) -> None:
  """ helper
  """
  table_Name = "locations_ratings"

  #class psycopg2.extras.LoggingConnection
  #  A connection that logs all queries to a file or logger object.

  #with psycopg2.connect( 
    # "dbname=test user=postgres"
  #  connection_Str 
  #, cursor_factory = psycopg2.extras.NamedTupleCursor
  #) as connection:

  #  connection.set_session( autocommit = True )

  if 1 == 1:
        
    # ?!? TypeError: argument 1 must be str, not psycopg2.extensions.connection
    #!#with connection.cursor() as cursor:
    with connection.cursor( 
    # name = "create_Table_Cursor" 
    ) as cursor:
      
      # Attempting to drop a table 
      # that does not exist is an error. 
      # Nevertheless, 
      # it is common in SQL script files 
      # to unconditionally try to drop each table 
      # before creating it, 
      # ignoring any error messages, 
      # so that the script works 
      # whether or not the table exists.
      
      print( f"About to create new '{table_Name}' table" )
      # psycopg2.ProgrammingError: relation "locations_ratings" already exists
      # if not present 
      # create a new table with a single column called "name"
      try:
        cursor\
          .execute(
            "CREATE TABLE "
            # Do not throw an error 
            # if a relation with the same name already exists. 
            # A notice is issued in this case. 
            # Note that there is no guarantee 
            # that the existing relation is anything 
            # like the one that would have been created.
            #?#"IF NOT EXISTS "
            "locations_ratings "
            #table_Name
            # NUMERIC( precision <- total digits: 8, scale <- digits in the fractional part: 6 )
            #              2 + 6 = 8
            # "latitude" : 19.793713,
            # "longitude": 86.513373,
            # CREATE TABLE test2 (b varchar(5));
            # INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit truncation
            # character varying(n), varchar(n)	<- variable-length with limit
            # character(n), char(n)	<- fixed-length, blank padded
            # text	<- variable unlimited length
            """
            ( 
              latitude char(10) NOT NULL, 
              longitude char(10) NOT NULL, 
              location text NOT NULL, 
              restaurant_name text NOT NULL, 
              rating text NOT NULL,
              PRIMARY KEY( latitude, longitude, restaurant_name ) 
            );"""
          )
      except psycopg2.ProgrammingError as pe:  
        print( f"When creating '{table_Name}' got: {pe}" )

        try:
          print( f"About to drop existing '{table_Name}' table" )
          cursor.execute( f"DROP TABLE {table_Name}" )
        except Exception as pe:  
          print( f"When dropping existed '{table_Name}' table got: {pe}" )
        else:
          # recursion 
          print( f"Existing '{table_Name}' table was successfully dropped" )
          print( f"About to recursively retry to create new '{table_Name}' table" )
          create_Table( connection )  
        finally:
          pass     
      else:
        print( f"New '{table_Name}' table was successfully created" )
        pprint( connection.notices )
      finally:
        pass     

  return None 

def add_Table_Record(
  connection#: psycopg2.extensions.connection
, record: Location_Rating   
, table_Name = "locations_ratings"
) -> None:
  """ helper
  """
  with connection.cursor( 
  #  name = "add_Table_Row_Cursor" 
  ) as cursor:

    print( f"About to insert values into new row in '{table_Name}' table" )
    #>>> cur.execute("INSERT INTO %s VALUES (%s)", ('numbers', 10))  # WRONG
    #>>> cur.execute(                                                # correct
    #...     SQL("INSERT INTO {} VALUES (%s)").format(Identifier('numbers')),
    #...     (10,))
    # mogrify(operation[, parameters])¶
    #   Return a query string 
    #   after arguments binding. 
    #   The string returned 
    #   is exactly the one 
    #   that would be sent 
    #   to the database 
    #   running the execute() method or similar.
    # The returned string is always a bytes string.
    #>>> cur.mogrify("INSERT INTO test (num, data) VALUES (%s, %s)", (42, 'bar'))
    #"INSERT INTO test (num, data) VALUES (42, E'bar')"
    try:
      if 1 == 0:
        print(
          "mogrify:"
        , cursor\
            .mogrify(
              f"INSERT INTO {table_Name} VALUES (%s, %s, %s, %s, %s);"
            , record
            )
        , sep = " "    
        ) 
        #>mogrify: b"INSERT INTO locations_ratings VALUES 
        # ('59.434', '24.7378113', 'CPMR+H2 Tallinn, Estonia', 'Hilton'
        # , '4.5 of 5 bubbles');"   
      cursor\
        .execute(
          f"INSERT INTO {table_Name} VALUES (%s, %s, %s, %s, %s);"
          #"INSERT INTO locations_ratings VALUES (%s, %s, %s, %s, %s);"
        , record
        #?#, tuple( record )
        )    
    except Exception as pe:  
      # when adding new record: 
      # Location_Rating(latitude='59.434', longitude='24.7378113'
      # , location='CPMR+H2 Tallinn, Estonia', restaurant_name='Hilton'
      #, rating='4.5 of 5 bubbles') 
      # in locations_ratings table got: 
      # not all arguments converted during string formatting
      print( 
        f"When adding new record: {record} in {table_Name} table got: {pe}" )
    else:
      pass 
      print( f"Values were successfully inserted into new row in '{table_Name}' table" )
    finally:
      pass     

  return None 

def convert_Coordinates_To_Location(
  # coordinates
  latitude: str # Decimal 
, longitude: str # Decimal 
) -> str:
  """"""
  return ""

def use_Location_Rating_Service(
  service_Url: str = "https://www.tripadvisor.com/"
  # coordinates
#  latitude: str # Decimal 
#, longitude: str # Decimal 
, headless: bool = True 
) -> Location_Rating:#str:
  """
  Centrs
  Central District, Riga, Latvia
  56.956583, 24.115240
  https://www.google.ru/maps/place/ + 56.956583, 24.115240 ( ? with escaping ? )
  X448+J3 Riga, Latvia

  click: Nearby ( button )
  type: Riits ( restaurant_name )
  url: https://www.google.ru/maps/place/Riits/@56.95242,24.1199173,17z
  address: Dzirnavu iela 72, Centra rajons, Rīga, LV-1050, Latvia
  plus code: X42C+XR Riga, Rīgas pilsēta, Latvia

  click: Nearby ( button )
  select: hotels 
  from list of options below pick:
  `Radisson Blu Latvija Conference & Spa Hotel, Riga` 
  url: `https://www.google.ru/maps/place/
    Radisson+Blu+Latvija+Conference+%26+Spa+Hotel,+Riga/
    @56.9538873,24.0989499,14z/`
  address: Elizabetes iela 55, Centra rajons, Rīga, LV-1010, Latvia
  plus code: X449+24 Riga, Rīgas pilsēta, Latvia

  paste to https://www.tripadvisor.com/ search:
  `Dzirnavu iela 72, Centra rajons, Rīga, LV-1050, Latvia Riits`
  does not work, it strips address to `Riga, Latvia, Europe`
  and goes to travel date picker 

  this works ? becuse hotels expected ? 
  `Radisson Elizabetes iela 55, Centra rajons, Rīga, LV-1010, Latvia` 
  document.querySelector('span.ui_bubble_rating').getAttribute("alt");
  "4.5 of 5 bubbles"
  """
  with web_Driver_Context( 
    headless = headless
  ) as driver:

    #logger.debug( f"driver.get( {url} )" )
    try:
      driver.set_page_load_timeout( 37 )
      driver.get( service_Url )
    except Exception as e:
      pass 
      #logger.error( 
      print(
        f"While getting page from the web `{service_Url}`: {e}" 
      , file = sys.stderr#stdout  
      )
    else:
      pass         
    finally:
      pass 

    #logger.debug( f"page title: {driver.title}" )  
    # element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id(“someId”))
    wait = WebDriverWait( driver, 37 #wait_Delay
      )
    input_Latitude = wait\
        .until( 
          EC
            #?#.visibility_of_element_located( 
            .presence_of_element_located(
            #>.element_to_be_clickable(	
              # instant, does not wait 
              #?#driver.find_element_by_id('TYPEAHEAD_LATITUDE')
              #>
              ( By.ID, 'TYPEAHEAD_LATITUDE' )
              #driver.find_element_by_class_name('c-garage-header__action')
              #>( By.CLASS_NAME, 'c-garage-header__action' ) 
              #( By.CSS_SELECTOR, 'div.c-garage-header__action' ) 
            ) 
        )  

    #option.get_attribute("value")
    # driver.execute_script(‘return document.title;’)
    # document.querySelector('input#TYPEAHEAD_LATITUDE').value = "59.434";
    #input_Longitude = driver.find_element_by_id('TYPEAHEAD_LONGITUDE')
    # document.querySelector('input#TYPEAHEAD_LONGITUDE').value = "24.7378113";
    driver.execute_script( 
      'document.querySelector("input#TYPEAHEAD_LONGITUDE").value = "24.7378113";' )

    # element.clear()
    input_Search_Text = driver.find_element_by_css_selector('input.typeahead_input')
    # element.send_keys("some text")
    # document.querySelector('input.typeahead_input').value = "Tchaikovsky Restaurant";
    input_Search_Text.send_keys( "Tchaikovsky Restaurant" )

    # document.getElementById("SUBMIT_HOTELS").click();  
    button_Submit = WebDriverWait( driver, 7 )\
      .until( lambda drv: drv.find_element_by_id( "SUBMIT_HOTELS" ) )
    button_Submit.click()  
    # last selected form.element:
    # element.submit()  
    # selenium.common.exceptions.NoSuchElementException: Message: no such element: 
    # Element was not in a form, so could not submit.
    #input_Search_Text.submit()
    
    # wait for redirect 
    WebDriverWait( driver, 17 )\
      .until( 
        # a custom Expected Condition
        lambda drv: drv.current_url != service_Url 
      )
    print( "driver.current_url:", driver.current_url ) 

    # document.querySelector('span.ui_bubble_rating').getAttribute("alt");
    #>"4.5 of 5 bubbles"
    span_Bubble_Rating = WebDriverWait( driver, 17 )\
      .until( 
        #>
        #lambda drv: drv.find_element_by_class_name( "ui_bubble_rating" ) 
        #
        lambda drv: drv.find_element_by_css_selector( "span.ui_bubble_rating" )         
        #EC
          #?#.visibility_of_element_located( 
          #.presence_of_element_located(
          #>.element_to_be_clickable(	
          #  ( By.CSS_SELECTOR, 'div.c-garage-header__action' ) 
          #)
      )

    location_Rating = span_Bubble_Rating.get_attribute( "alt" ) 
    print( "location_Rating:", location_Rating ) 
      
  return True#""

def main(
  longitude: str 
, latitude: str
, restaurant_name: str   
) -> None:#str:
  """
  """
  print( 
    f"longitude: {longitude}, longitude: {longitude}"
    f", restaurant_name: {restaurant_name}" 
  )

  return None 

get_Location_Rating = lambda la, lo, f_name: None 

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
  if 1 == 0:
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
      description = "Extract | scrap location rating data from public web service"
    )
  #parser.add_argument( "-C", '--coordinates', nargs = 2, metavar = ( 'longitude', 'latitude' ) )  
  parser.add_argument( 
    #?#  "LA"
      "latitude"
    , type = str, help = "the location latitude" 
    )
  parser.add_argument( 
    #?#  "LO"
      "longitude"
    , type = str, help = "the location longitude" 
    )
  parser.add_argument( 
    #?#  "RN"
      "restaurant_name"
    #>  "-RN"
    #>, "--restaurant_name"
    #, type = str
    , help = "the restaurant name to rate" 
    #>, required = True
    #, action = 'store'
    )

  args = parser.parse_args()
  
  #parser.print_help()
  main( 
    # TypeError: main() argument after ** must be a mapping, not Namespace
    **vars( args ) 
  )
