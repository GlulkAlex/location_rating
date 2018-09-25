import unittest
from location_rating import (
  main 
, create_Table  
)
import sys
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
  def test_output_capture_with_redirect_stdout(self):
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

  #@unittest.skip("skipping demo")
  def test_Create_DB_Table( self ):

    DSN = 'dbname=test_db'
    table_Name = "locations_ratings"

    # psycopg2.connect(dsn=None, connection_factory=None, cursor_factory=None, async=False, **kwargs)
    with psycopg2.connect( 
      dsn = DSN
    #?#, cursor_factory = NamedTupleConnection 
    , cursor_factory = psycopg2.extras.DictCursor
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
        self.assertEqual( 
            cursor.fetchall()
            , [
              #( 10, )
            ] 
          )        

  @unittest.skip("skipping demo")
  def test_Store_State_In_DB_Table( self ):

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
