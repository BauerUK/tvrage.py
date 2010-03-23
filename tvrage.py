__author__="Bauer"
__date__ ="$22-Mar-2010 21:22:37$"

import urllib
from datetime import datetime, date, time
from elementtree.ElementTree import XML, fromstring

URL_SEARCH = "http://services.tvrage.com/feeds/search.php?show=%(show)s"
URL_SHOWINFO = "http://services.tvrage.com/feeds/full_show_info.php?sid=%(id)s"
URL_TVRAGE_ROOT = "http://www.tvrage.com"

DATE_SHOW = "%b/%d/%Y"
DATE_EPISODE = "%Y-%m-%d"

def GetShowByName(showName):
  """
  Searches for a show by a given name. 
  Returns the full information of the first result or None if there are no results.
  """
  results = Search(showName)

  if results:
    return GetShowByID(results[0].ID)
  else:
    return None

def GetShowByID(showID):
  """
  Gets a show by a TVRage ID.
  Returns the full information (Show object) or None if the ID is invalid.
  """
  # tvrage provides no/inconsistent error-reporting so we must try/except
  try:
    url = URL_SHOWINFO % {'id':showID}
    uf = urllib.urlopen(url)
    xml = uf.read()
    xShow = fromstring(xml)
    return Show(xShow)
  except:
    return None
  
def Search(query):
  """
  Searches for a show based on a given query (the show name).
  Returns a Show object result if the result is succesful, or None if unsuccesful.
  """
  # compile the search url
  url = URL_SEARCH % {'show':query}

  # grab the string xml results
  uf = urllib.urlopen(url)
  xml = uf.read()

  # load an xml tree object from the search results
  xResults = fromstring(xml)

  # compile results
  results = []
  for e in xResults.findall("show"):
    results.append(SearchResult(e))

  return results

class Show(object):

  def __init__(self, element):
    
    self.ID = element.findtext("showid")
    self.Name = element.findtext("name")
    self.Link = URL_TVRAGE_ROOT + element.findtext("showlink")
    self.Country = element.findtext("origin_country")
    
    started = element.findtext("started")
    if started:
      self.Started = strptime(started, DATE_SHOW)

    ended = element.findtext("ended")
    if ended:
      self.Ended = strptime(ended, DATE_SHOW)

    self.Image = URL_TVRAGE_ROOT + element.findtext("image")
    self.Seasons = element.findtext("seasons")
    self.Status = element.findtext("status")
    self.Class = element.findtext("classification")
    self.Genres = [genre.text for genre in element.find("genres").findall("genre")]
    self.Runtime = element.findtext("runtime");
    networkElement = element.find("network");
    self.Network = {networkElement.get('country') : networkElement.text}
    self.AirTime = element.findtext("airtime");
    self.AirDay = element.findtext("airday");
    self.TimeZone = element.findtext("timezone");

    self.AKA = {}
    akas = element.find("akas").findall("aka");
    for aka in akas:
      self.AKA[aka.get('country')] = aka.text

    self.Episodes = []

    seasons = element.find("Episodelist").findall("Season")

    for season in seasons:
      seasonnum = season.get('no')
      for episode in season.findall('episode'):
        self.Episodes.append(Episode(episode, seasonnum, false))

    specials = element.find("Episodelist").findall("Special")

    for special in specials:
      self.Episodes.append(Episode(special, special.findtext("season"), true))

class Episode(object):
  
  def __init__(self, element, season, special):
    self.SeasonNumber = season
    self.Special = special

    if not special:
      self.EpisodeNumber = element.findtext("seasonnum")
    else:
      self.EpisodeNumber = 0
      
    self.TotalEpisodeNumber = element.findtext("epnum")
    self.ProductionNumber = element.findtext("prodnum")

    airdate = element.findtext("airdate")
    if airdate:
      self.AirDate = strptime(element.findtext("airdate"), DATE_EPISODE)

    self.Link = URL_TVRAGE_ROOT + element.findtext("link")
    self.Title = element.findtext("title")
    self.ScreenCap = URL_TVRAGE_ROOT + element.findtext("screencap")

class SearchResult(object):
  
  def __init__(self, element):
    self.ID = element.findtext("showid")
    self.Name = element.findtext("name")
    self.Link = URL_TVRAGE_ROOT + element.findtext("link")
    self.Country = element.findtext("country")

    started = element.findtext("started")
    if started:
      self.Started = strptime(started, DATE_SHOW)

    ended = element.findtext("ended")
    if ended:
      self.Ended = strptime(ended, DATE_SHOW)

    self.Seasons = element.findtext("seasons")
    self.Status = element.findtext("status")
    self.Class = element.findtext("classification")
    self.Genres = [genre.text for genre in element.find("genres").findall("genre")]

if __name__ == "__main__":
    show = GetShowByName("lost")
    print show.ID
    print show.Name
    print show.Link
    print show.Country
    print show.Started
    print show.Ended
    print show.Seasons
    print show.Status
    print show.Class
    print show.Genres
    print show.Runtime
    print show.Network
    print show.AirTime
    print show.AirDay
    print show.TimeZone
    print show.AKA