import unittest
from location_rating import (
  main 
, get_Connection_DSN   
, create_Table  
, Location_Rating
, add_Table_Record
, get_Location_Rating 
)
import sys
import os
#?#from cStringIO import StringIO
from io import StringIO
from contextlib import contextmanager
from contextlib import redirect_stdout
from pprint import pprint, pformat

import psycopg2
from psycopg2 import extras
from psycopg2.extras import NamedTupleConnection
#?#from psycopg2.extensions import connection as P2_Connection
#
#
@contextmanager
def capture(
  command
, *args, **kwargs
):
  """
  a factory function 
  for 'with' statement context managers, 
  without needing 
  to create a class 
  or separate __enter__() and __exit__() methods.

  This ( decorated ) function 
  must return a generator-iterator when called.
  """
  # acquire resource:
  # swap 
  #out, sys.stdout = sys.stdout, StringIO()
  out = sys.stdout
  sys.stdout = StringIO()

  try:
    command(*args, **kwargs)
    sys.stdout.seek(0)
    # This iterator must yield exactly one value, 
    # which will be bound 
    # to the targets 
    # in the 'with' statement’s 'as' clause, 
    # if any.
    yield sys.stdout.read()
  finally:
    # release resource:   
    sys.stdout = out

#@unittest.skip("showing class skipping")
class Test_Helpers( unittest.TestCase ):
  """
  #?#python3.6 -m unittest -v test__location_rating
  with __init__.py
  #>$ python -m unittest discover
  """

  def setUp(self):
    self._conns = []
          
  def tearDown(self):
    # close the connections used in the test
    for conn in self._conns:
      # with closed 
      # self.assertRaises(psycopg2.InterfaceError, f) 
      if not conn.closed:
        conn.close()

  @unittest.skip("skipping capture contextmanager use test")
  def test_and_capture_output(self):

    with capture(
      # callable
      print
    #, *args, **kwargs
    , "42"
    ) as output:
      self.assertEqual( "Expected output", output )

  @unittest.skip("skipping redirect_stdout use test")
  def test__output_capture_with_redirect_stdout(self):
    # file-like object
    flo = (
      #io.\
        StringIO()
    )

    with redirect_stdout(flo):
      #help(pow)
      print( "42" )

    #s = flo.getvalue()  
    self.assertEqual( "Expected output", flo.getvalue() )

  #@unittest.skip("skipping create_Table test")
  def test__Get_Connection_DSN( self ):
    expected_Result = 'dbname=test_db'
    DSN = get_Connection_DSN()

    self.assertEqual( DSN, expected_Result )
    self.assertEqual( 
        os.getenv( 
          "PostgreSQL_Dev_DSN"
        , default = None 
        )
      , expected_Result 
      )

  @unittest.skip("skipping create_Table test")
  def test__Create_DB_Table( self ):

    DSN = get_Connection_DSN()#'dbname=test_db'
    table_Name = "locations_ratings"

    # psycopg2.connect(dsn=None, connection_factory=None, cursor_factory=None, async=False, **kwargs)
    with psycopg2.connect( 
      dsn = DSN
    #?#, cursor_factory = NamedTupleConnection 
    #>, cursor_factory = psycopg2.extras.DictCursor
    , cursor_factory = psycopg2.extras.NamedTupleCursor
    ) as connection:

      #>print( "dir( psycopg2.extensions )", dir( psycopg2.extensions ), sep = "\n" )
      if 1 == 0:
        print( 
          "help( psycopg2.extensions.connection )"
        , help( psycopg2.extensions.connection )
        , sep = "\n" 
        )
        #> class connection(builtins.object)

      if 1 == 0:
        # TypeError: isinstance() arg 2 must be a type or tuple of types
        # AssertionError: 
        #   <connection object at 0x7fb2081149c8; dsn: 'dbname=test_db', closed: 0> 
        #   is not an instance of <class 'type'>
        self.assertIsInstance(
          #  obj
            connection 
          #, cls
          #!#, psycopg2.extensions.connection
          #?#, type( psycopg2.extensions.connection )
          #?#, psycopg2.extensions.connection.__class__
          #!#, P2_Connection 
          #!#, object 
          , int 
          )

      connection.set_session( autocommit = True )

      create_Table( connection )
    
      with connection.cursor( 
      #  name = "test_Cursor" 
      #?#, cursor_factory = NamedTupleConnection  
        cursor_factory = psycopg2.extras.NamedTupleCursor
      ) as cursor:

        if 1 == 0:
          self.assertIsInstance(
            #  obj
              cursor 
            #, cls
            #!#, psycopg2.extensions.connection.cursor
            , psycopg2.extensions.cursor.__class__
            )

        cursor.execute( "select * from locations_ratings;" )

        self.assertEqual( cursor.rowcount, 0 )

        # In order to pass a Python object 
        # to the database 
        # as query argument you can use the Json adapter:
        #curs.execute("insert into mytable (jsondata) values (%s)", [Json({'a': 100})])
        # Reading from the database, 
        # json and jsonb values 
        # will be automatically converted 
        # to Python objects.
        self.assertEqual( 
            cursor.fetchall()
            , [
              #( 10, )
            ] 
          )        

  #@unittest.skip("skipping demo")
  def test__Add_Row_To_DB_Table( self ):

    DSN = get_Connection_DSN()
    table_Name = "locations_ratings"

    with psycopg2.connect( 
      dsn = DSN
    #>, cursor_factory = psycopg2.extras.DictCursor
    # fetch*() methods will return named tuples instead of regular tuples
    # e.g. 
    # Record(id=1, num=100, data="abc'def")
    #>, cursor_factory = psycopg2.extras.NamedTupleCursor
    ) as connection:
      
      connection.set_session( autocommit = True )

      record = Location_Rating( 
        latitude = "59.434", longitude = "24.7378113"
      , location = "CPMR+H2 Tallinn, Estonia"
      , restaurant_name = "Hilton"
      , rating = "4.5 of 5 bubbles"
      )  
    
      with connection.cursor( 
      #  name = "test_Cursor" 
      #?#, cursor_factory = NamedTupleConnection  
      #  cursor_factory = psycopg2.extras.NamedTupleCursor
      ) as cursor:

        #create_Table( connection )
        # to remove table:
        #?#cursor.execute( f"DROP TABLE {table_Name}" )
        # to remove rows:
        # DELETE FROM products WHERE price = 10;
        cursor.execute( f"delete from {table_Name}" )

        add_Table_Record( connection, record )

        cursor.execute( "select * from locations_ratings;" )

        self.assertEqual( cursor.rowcount, 1 )
        self.assertEqual( 
              [ tuple( sv.rstrip() for sv in row ) for row in cursor.fetchall() ]
            , [
              #( 10, )
              #Record( latitude='59.434    '
              #, longitude='24.7378113', location='CPMR+H2 Tallinn, Estonia'
              #, restaurant_name='Hilton', rating='4.5 of 5 bubbles' )
              #>
              tuple( record )
              #?#record 
            ] 
          )        

  @unittest.skip("skipping demo")
  def test__Store_State_In_DB_Table( self ):

    DSN = 'dbname=test_db'
    print( "Opening ( new ) connection using dsn:", DSN )

    if 1 == 0:
      conn = psycopg2.connect( DSN )
      print( "Encoding for this connection is", conn.encoding )

      curs = conn.cursor()
      #>>> cur.execute("CREATE TABLE foo (id serial PRIMARY KEY);")
      #>>> pprint(conn.notices)
      try:
        curs.execute("CREATE TABLE test_copy (fld1 text, fld2 text, fld3 int4)")
      except:
        # if exist already 
        conn.rollback()
        curs.execute("DROP TABLE test_copy")
        # to enforce table structure | schema 
        curs.execute("CREATE TABLE test_copy (fld1 text, fld2 text, fld3 int4)")

      conn.commit()

      #with self.connect( connection_factory = MyConn ) as conn:
      with psycopg2.connect( 
        DSN
        #?#connection_factory = NamedTupleConnection 
      ) as conn:
        curs = conn.cursor()
        curs.execute("insert into test_with values (10)")

      curs = self.conn.cursor()
      curs.execute("select * from test_with")
      self.assertEqual(curs.fetchall(), [(10,)])

      # clear table 
      curs.execute("delete from test_copy")
      conn.commit()
      print( "Total number of rows deleted :", curs.rowcount )

      # clear DB from temp data
      curs.execute("DROP TABLE test_copy")
      conn.commit()
      #conn.rollback()
      conn.close()
      #sys.exit(0)

  @unittest.skip("skipping main final test")
  def test__Get_Location_Rating( self ):
    """ final test 
    """
    flo = StringIO()

    DSN = get_Connection_DSN()
    table_Name = "locations_ratings"

    with psycopg2.connect( 
      dsn = DSN
    #>, cursor_factory = psycopg2.extras.DictCursor
    # fetch*() methods will return named tuples instead of regular tuples
    # e.g. 
    # Record(id=1, num=100, data="abc'def")
    #>, cursor_factory = psycopg2.extras.NamedTupleCursor
    ) as connection:
      
      connection.set_session( autocommit = True )

      record = Location_Rating( 
        latitude = "59.434", longitude = "24.7378113"
      , location = "CPMR+H2 Tallinn, Estonia"
      , restaurant_name = "Hilton"
      , rating = "4.5 of 5 bubbles"
      )  
    
      with connection.cursor( 
      #  name = "test_Cursor" 
      #?#, cursor_factory = NamedTupleConnection  
      #  cursor_factory = psycopg2.extras.NamedTupleCursor
      ) as cursor:

        with redirect_stdout( flo ):

          get_Location_Rating( 
            record.latitude, record.longitude
          , record.restaurant_name 
          )

        #s = flo.getvalue()  
        self.assertEqual( "Expected output", flo.getvalue() )

        #test_db=# select rating from locations_ratings 
        #where latitude = '59.434' and longitude = '24.7378113' 
        #and location = 'CPMR+H2 Tallinn, Estonia';
        #     rating      
        #------------------
        #4.5 of 5 bubbles
        #(1 row)

        # Named arguments are supported 
        # using '%(name)s' placeholders in the query 
        # and specifying the values into a mapping. 
        # Using named arguments allows 
        # to specify the values in any order 
        # and to repeat the same value in several places in the query:
        cursor.execute( 
            "select rating "
            "from locations_ratings "
            "where "
            "latitude = %s "
            "and longitude = %s "
            "and restaurant_name = %s "
            ";" 
          , ( record.latitude, record.longitude, record.restaurant_name )  
          )

        self.assertEqual( cursor.rowcount, 1 )
        self.assertEqual( 
              # Fetch the next row of a query result set, 
              # returning a single tuple, 
              # or None when no more data is available:
              cursor.fetchone()
            , ( record.rating, )
          )        
