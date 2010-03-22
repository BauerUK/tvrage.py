__author__="Bauer"
__date__ ="$22-Mar-2010 21:22:37$"

import urllib
from datetime import datetime, date, time

url_quickinfo = "http://services.tvrage.com/tools/quickinfo.php?show=%(show)s"
format_shortdate = "%b/%d/%Y"
def search(show):
  """
    Retrieves basic information about a show.
  """

  url = url_quickinfo % {'show':show}
  
  uf = urllib.urlopen(url)
  result = uf.read()

  if result.startswith("<pre>"):
    result = result[5:]

  if result.endswith("</pre>"):
    result = result[:-6]

  return Show.parse(result)


class Show(object):

  def get_id(self):
    return self._id
  ID = property(get_id)
  """The TVRage site ID"""

  def get_name(self):
    return self._name
  Name = property(get_name)
  """The name of the show"""

  def get_url(self):
    return self._url
  URL = property(get_url)
  """The TVRage url for the show"""

  def get_premiered(self):
    return self._premiered
  YearPremiered = property(get_premiered)
  """The year the show premiered"""

  def get_started(self):
    return self._started
  DateStarted = property(get_started)
  """The date the show started"""

  def get_ended(self):
    return self._ended
  DateEnded = property(get_ended)
  """The date the show ended"""

  def get_latest(self):
    return self._latest
  EpisodeLatest = property(get_latest)
  """The latest (last aired) episode"""

  def get_next(self):
    return self._next
  EpisodeNext = property(get_next)
  """The next episode to air"""

  def get_country(self):
    return self._country
  Country = property(get_country)
  """The country the show airs in"""

  def get_status(self):
    return self._status
  Status = property(get_status)
  """The show status (cancelled, ended, returning etc.)"""

  def get_class(self):
    return self._class
  Classification = property(get_class)
  """The show classification (scripted, reality etc.)"""

  def get_genres(self):
    return self._genres
  Genres = property(get_genres)
  """The genre(s) of the show (action, adventure, drama etc.)"""

  def get_network(self):
    return self._network
  Network = property(get_network)
  """The network on which the show airs"""

  def get_runtime(self):
    return self._runtime
  Runtime = property(get_runtime)
  """How long the show airs for (minutes)"""

  @staticmethod
  def parse(result):
    show = Show()
    for line in result.splitlines(): 
      property = line.partition('@')
      key = property[0]
      value = property[2]

      if key == "Show ID" and value:
        show._id = value
      if key == "Show Name" and value:
        show._name = value
      if key == "Show URL" and value:
        show._url = value
      if key == "Premiered" and value:
        show._premiered = value
      if key == "Started":
        show._started = datetime.strptime(value, format_shortdate)
      if key == "Ended" and value:
        show._ended = datetime.strptime(value, format_shortdate)
      if key == "Latest Episode" and value:
        show._latest = Episode.parse(value)
      if key == "Next Episode" and value:
        show._next = Episode.parse(value)
      if key == "Country" and value:
        show._country = value
      if key == "Status" and value:
        show._status = value
      if key == "Classification" and value:
        show._class = value
      if key == "Genres" and value:
        show._genres = value.split(' | ')
      if key == "Network" and value:
        show._network = value
      if key == "Runtime" and value:
        show._runtime = value

    return show

class Episode(object):

  def get_season(self):
    return self._season
  Season = property(get_season)
  """The season number"""""

  def get_ep(self):
    return self._ep
  Episode = property(get_ep)
  """The episode number"""

  def get_title(self):
    return self._title
  Title = property(get_title)
  """The episode title"""

  def get_airdate(self):
    return self._airdate
  AirDate = property(get_airdate)
  """The episode airdate"""

  @staticmethod
  def parse(epline):
    ep = Episode()
    epdata_all = epline.split('^')

    epdata_ep = epdata_all[0].partition('x')
    ep._season = epdata_ep[0]
    ep._ep = epdata_ep[2]

    ep._title = epdata_all[1]
    ep._airdate = datetime.strptime(epdata_all[2], format_shortdate)

    return ep

if __name__ == "__main__":

    show = search("lost")

    print show.Name
