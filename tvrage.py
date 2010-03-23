__author__="Bauer"
__date__ ="$22-Mar-2010 21:22:37$"

from urllib import urllib
from datetime import datetime, date, time
import elementtree.ElementTree

url_search = "http://services.tvrage.com/feeds/search.php?show=%(show)s"
format_shortdate = "%b/%d/%Y"

def search(query):
  """
    Searches for a show based on a given query (the show name).

    Returns a Show object if the result is succesful, or None if unsuccesful.
  """

  url = url_search % {'show':query}

  return Show.parse(result)

class Show(object):

  def __init__(self):
    self._ShowID = 0 # TODO
  def ShowID():
    doc = "The ShowID property."
    def fget(self):
      return self._ShowID
  

  @staticmethod
  def load(result):
    show = Show()    

    return show

class Episode(object):

  def __init__(self):
    print "Not yet implemented."

if __name__ == "__main__":

    show = search("lost")

    print show.Name
