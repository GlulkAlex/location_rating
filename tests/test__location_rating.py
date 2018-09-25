import unittest
from location_rating import (
  main 
)
import sys
#?#from cStringIO import StringIO
from io import StringIO
from contextlib import contextmanager
from contextlib import redirect_stdout
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

  @unittest.skip("skipping capture contextmanager use test")
  def test_and_capture_output(self):

    with capture(
      # callable
      print
    #, *args, **kwargs
    , "42"
    ) as output:
      self.assertEqual( "Expected output", output )

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

  @unittest.skip("skipping demo")
  def test_State_Store_Dict( self ):
    pass
