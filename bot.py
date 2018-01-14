from credentials import *
from bs4 import BeautifulSoup
import threading
import requests
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
oldCall = None
calls = []

def checkCalls():
  threading.Timer(10, checkCalls).start()

  url = "http://ws.ocsd.org/CrimeCalls/default.aspx"

  html = requests.post(url).text
  soup = BeautifulSoup(html, 'html.parser')
  viewState = soup.find("input", {"name":"__VIEWSTATE"})['value']
  viewStateGenerator = soup.find("input", {"name":"__VIEWSTATEGENERATOR"})['value']
  eventValidation = soup.find("input", {"name":"__EVENTVALIDATION"})['value']

  headers = {
      'Origin': 'http://ws.ocsd.org',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.8',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.51 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Cache-Control': 'max-age=0',
      'Referer': 'http://ws.ocsd.org/CrimeCalls/default.aspx',
      'Connection': 'keep-alive',
      'DNT': '1',
  }
  data = {
    '__VIEWSTATE': '/wEPDwUKLTQ2ODQxMzY4Nw9kFgICAw9kFgQCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQZhZ2VuY3keDkRhdGFWYWx1ZUZpZWxkBQRjb2RlHgtfIURhdGFCb3VuZGdkDxYMAgECAgIDAgQCBQIGAgcCCAIJAgoCCwIMFgwQBRlBTkFIRUlNIFBPTElDRSBERVBBUlRNRU5UBQVBTkFQRGcQBRxCVUVOQSBQQVJLIFBPTElDRSBERVBBUlRNRU5UBQNCVVBnEAUZQ1lQUkVTUyBQT0xJQ0UgREVQQVJUTUVOVAUDQ1lQZxAFIUZPVU5UQUlOIFZBTExFWSBQT0xJQ0UgREVQQVJUTUVOVAUDRlRWZxAFG0ZVTExFUlRPTiBQT0xJQ0UgREVQQVJUTUVOVAUDRlVMZxAFGkxBIEhBQlJBIFBPTElDRSBERVBBUlRNRU5UBQNMQUhnEAUeTE9TIEFMQU1JVE9TIFBPTElDRSBERVBBUlRNRU5UBQNMQUxnEAUaTEEgUEFMTUEgUE9MSUNFIERFUEFSVE1FTlQFA0xQTWcQBSJPUkFOR0UgQ09VTlRZIFNIRVJJRkYnUyBERVBBUlRNRU5UBQRPQ1NEZxAFHFNFQUwgQkVBQ0ggUE9MSUNFIERFUEFSVE1FTlQFA1NMQmcQBRhUVVNUSU4gUE9MSUNFIERFUEFSVE1FTlQFA1RVU2cQBR1XRVNUTUlOU1RFUiBQT0xJQ0UgREVQQVJUTUVOVAUDV1NNZ2RkAgUPPCsADQEADxYEHwJnHgtfIUl0ZW1Db3VudAIJZBYCZg9kFhQCAQ9kFhJmDw8WAh4EVGV4dAUJNTY0NzMwNzA4ZGQCAQ8PFgIfBAUGJm5ic3A7ZGQCAg8PFgIfBAUQRk9MTE9XIFVQIFJFUE9SVGRkAgMPDxYCHwQFBEZXVVBkZAIEDw8WAh8EBRQyOTcwMCBCTEsgTUVMSU5EQSBSRGRkAgUPDxYCHwQFAlJTZGQCBg8PFgIfBAUET0NTRGRkAgcPDxYCHwQFFDEvMTIvMjAxNyA3OjQ4OjA2IFBNZGQCCA8PFgIfBAUDbi9hZGQCAg9kFhJmDw8WAh8EBQk1NjQ3MzA3MDlkZAIBDw8WAh8EBQYmbmJzcDtkZAICDw8WAh8EBQ5TVE9MRU4gVkVISUNMRWRkAgMPDxYCHwQFAzUwM2RkAgQPDxYC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',
    '__VIEWSTATEGENERATOR': 'EA26F1DB',
    '__EVENTVALIDATION': '/wEWDwKkreubDwLop9OLBgL+lu+eCwKwnZnNDQK/nanNDQKeltLNDgLwjuPOAwLeo9r7CgLKjtPOAwLVtbHRCQLE0cjoAgKlh5TPBALf0fCNDAKqtYXRCQKln/PuCvWXn5vpKvYJrRMamnxIS3z0O9pd',
    'ddlAgencies': 'OCSD',
    'btnSearch.x': '31',
    'btnSearch.y': '19'
  }
  html = requests.post(url + "?ddlAgencies=OCSD&btnSearch.x=43&btnSearch.y=18", headers=headers, data=data).text


  global oldCall
  global calls
  soup = BeautifulSoup(html, 'html.parser')
  table = soup.find("table", attrs={"class":"tableCalls"})
  headings = [th.get_text() for th in table.find("tr").find_all("th")]

  for row in table.find_all('tr'):
      dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
      calls.append(dataset)

  if (oldCall != calls[1][7][1]):
      fullname = ""
      hashtag = ""
      if (calls[1][6][1] == "ANAPD"):
          fullname = "Anaheim PD"
          hashtag = "#Anaheim"
      elif (calls[1][6][1] == "BUP"):
          fullname = "Buena Park PD"
          hashtag = "#BuenaPark"
      elif (calls[1][6][1] == "CYP"):
          fullname = "Cypress PD"
          hashtag = "#Cypress"
      elif (calls[1][6][1] == "FTV"):
          fullname = "Fountain Valley PD"
          hashtag = "#FountainValley"
      elif (calls[1][6][1] == "FUL"):
          fullname = "Fullerton PD"
          hashtag = "#Fullerton"
      elif (calls[1][6][1] == "LAH"):
          fullname = "La Habra PD"
          hashtag = "#LaHabra"
      elif (calls[1][6][1] == "LAL"):
          fullname = "Los Alamitos PD"
          hashtag = "#LosAlamitos"
      elif (calls[1][6][1] == "LPM"):
          fullname = "La Palma PD"
          hashtag = "#LaPalma"
      elif (calls[1][6][1] == "SLB"):
          fullname = "Seal Beach PD"
          hashtag = "#SealBeach"
      elif (calls[1][6][1] == "TUS"):
          fullname = "Tustin PD"
          hashtag = "#Tustin"
      elif (calls[1][6][1] == "WSM"):
          fullname = "Westminster PD"
          hashtag = "#Westminster"
      elif (calls[1][5][1] == "LF"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LakeForest"
      elif (calls[1][5][1] == "YL"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#YorbaLinda"
      elif (calls[1][5][1] == "MV"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#MissionViejo"
      elif (calls[1][5][1] == "RS"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#RanchoSantaMargarita"
      elif (calls[1][5][1] == "SA"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#SantaAna"
      elif (calls[1][5][1] == "GG"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#GardenGrove"
      elif (calls[1][5][1] == "SC"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#SanClemente"
      elif (calls[1][5][1] == "AV"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#AlisoViejo"
      elif (calls[1][5][1] == "LN"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LagunaNigel"
      elif (calls[1][5][1] == "ST"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#Stanton"
      elif (calls[1][5][1] == "NH"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#NewportBeachHarbor"
      elif (calls[1][5][1] == "RO"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#Rossmoor"
      elif (calls[1][5][1] == "CN"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#ClevlandForest"
      elif (calls[1][5][1] == "CS"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#ClevlandForest"
      elif (calls[1][5][1] == "CZ"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#CotoDeCaza"
      elif (calls[1][5][1] == "JW"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#JohnWayneAirport"
      elif (calls[1][5][1] == "LM"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LaMirada"
      elif (calls[1][5][1] == "LD"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LanderaRanch"
      elif (calls[1][5][1] == "LH"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LagunaHills"
      elif (calls[1][5][1] == "FL"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#LasFlores"
      elif (calls[1][5][1] == "RV"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#RanchoMissionViejo"
      elif (calls[1][5][1] == "SJ"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#SanJuanCapistrano"
      elif (calls[1][5][1] == "SI"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#SilveradoCanyon"
      elif (calls[1][5][1] == "SN"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#SunsetBeachHarbor"
      elif (calls[1][5][1] == "TC"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#TrabucoCanyon"
      elif (calls[1][5][1] == "VP"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#VillaPark"
      elif (calls[1][5][1] == "DP"):
          fullname = "Orange County Sheriff's Department"
          hashtag = "#DanaPoint"
      else:
          fullname = calls[1][6][1]
          hashtag = "#OrangeCounty"
      try:
          print "CALL: [" + calls[1][3][1] + "] " + calls[1][2][1] + " \nADDR: " + calls[1][4][1] + ", " + calls[1][5][1] + " \nD/T: " + calls[1][7][1] + " \n" + hashtag
          api.update_status("CALL: [" + calls[1][3][1] + "] " + calls[1][2][1] + " \nADDR: " + calls[1][4][1] + ", " + calls[1][5][1] + " \nD/T: " + calls[1][7][1] + " \n" + hashtag)
      except:
          print "ERROR"

  oldCall = calls[1][7][1]
  calls = []
  print oldCall
checkCalls()
