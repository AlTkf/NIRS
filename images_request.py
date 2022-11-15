import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
import json

pp = PrettyPrinter()

def request_image():
  API_Root = "https://images-api.nasa.gov/search"
  parameters = {
      'media_type':'image'
  }
  response = requests.get(API_Root, params=parameters).json()
  #return pp.pprint(response)
  return response

for key in request_image()['collection']['items'][0]['data']:
  print('\n\n')
  print('id:', request_image()['collection']['items'][0]['data'][0]['nasa_id'])
  print('title:', request_image()['collection']['items'][0]['data'][0]['title'])
  print('keyword:', request_image()['collection']['items'][0]['data'][0]['keywords'])
  print('description:', request_image()['collection']['items'][0]['data'][0]['description'])
  print('image link:', request_image()['collection']['items'][0]['links'][0]['href'])


 
