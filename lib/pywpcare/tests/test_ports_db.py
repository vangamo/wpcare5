import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from pywpcare.ports.db.db import *

class TestSiteClass():

  def test_connection(self):
    assert DB.get_connection is not None
    
    result = DB.get_connection()

    assert result is not None