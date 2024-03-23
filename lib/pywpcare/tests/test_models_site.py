import sys
import os
print(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from pywpcare.models.site import Site

class TestSiteClass():

  def test_init(self):
    result = Site()

    assert result is not None