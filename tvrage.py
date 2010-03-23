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
    result = results[0]
    return GetShowByID(result.ID)
  else:
    return None

def GetShowByID(showID):
  """
  Gets a show by a TVRage ID.
  Returns the full information (Show object) or None if the ID is invalid.
  """
  # tvrage provides no/inconsistent error-reporting so we must try/except
  url = URL_SHOWINFO % {'id':showID}
  uf = urllib.urlopen(url)
  xml = uf.read()
  xShow = fromstring(xml)
  return Show(xShow)

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
    self.Started = element.findtext("started")
    self.Ended = element.findtext("ended")
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

    xEpisodelist = element.find("Episodelist")

    seasons = xEpisodelist.findall("Season")

    for season in seasons:
      seasonnum = season.get('no')
      for episode in season.findall('episode'):
        self.Episodes.append(Episode(episode, seasonnum, False))

    specials = xEpisodelist.find("Special").findall("episode")

    for episode in specials:
      self.Episodes.append(Episode(episode, episode.findtext("season"), True))

class Episode(object):
  
  def __init__(self, element, season, special):
    self.SeasonNumber = season
    self.Special = special

    if not special:
      self.EpisodeNumber = element.findtext("seasonnum")
    else:
      self.EpisodeNumber = "0"
      
    self.TotalEpisodeNumber = element.findtext("epnum")
    self.ProductionNumber = element.findtext("prodnum")

    airdate = element.findtext("airdate")
    if airdate:
      self.AirDate = datetime.strptime(element.findtext("airdate"), DATE_EPISODE)

    link = element.findtext("link")
    if link:
      self.Link = URL_TVRAGE_ROOT + link
      
    self.Title = element.findtext("title")

    screencap = element.findtext("screencap")
    if screencap:
      self.ScreenCap = URL_TVRAGE_ROOT + screencap

class SearchResult(object):
  
  def __init__(self, element):
    self.ID = element.findtext("showid")
    self.Name = element.findtext("name")
    self.Link = URL_TVRAGE_ROOT + element.findtext("link")
    self.Country = element.findtext("country")
    self.Started = element.findtext("started")
    self.Ended = element.findtext("ended")
    self.Seasons = element.findtext("seasons")
    self.Status = element.findtext("status")
    self.Class = element.findtext("classification")
    self.Genres = [genre.text for genre in element.find("genres").findall("genre")]

if __name__ == "__main__":
    show = GetShowByName("lost")