import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
# import jsonirt
import psycopg2
import socket

pp = PrettyPrinter()

def request_image():
  API_Root = "https://images-api.nasa.gov/search"
  parameters = {
      'media_type' : 'image'
  }
  response = requests.get(API_Root, params=parameters).json()
  # return pp.pprint(response)
  return response

server = socket.gethostbyname(socket.gethostname())

data = request_image()

try:
    connection = psycopg2.connect(user="postgres",
                                  password="Genesis-01",
                                  # host="str(server)",
                                  port="5432",
                                  database="nasa")
    
    if connection:
      print('Connection established')
    
    cursor = connection.cursor()

    for key in data['collection']['items']:
      postgres_insert_query = "INSERT INTO data (id, title, description, image_link) VALUES (%s,%s,%s,%s)"
      record_to_insert = (key['data'][0]['nasa_id'], key['data'][0]['title'], key['data'][0]['description'], key['links'][0]['href'])
      cursor.execute(postgres_insert_query, record_to_insert)


except psycopg2.Error as error:
    print("Connection error:", error.pgerror)

finally:
  connection.commit()
  cursor.close()
  connection.close()
  print('Connection closed')

# image_info = {
#   'id' : [],
#   'title' : [],
#   'description' : [],
#   'image link' : [],
# }

# for key in data['collection']['items']:
#   image_info['id'].append(key['data'][0]['nasa_id'])
#   image_info['title'].append(key['data'][0]['title'])
#   image_info['description'].append(key['data'][0]['description'])
#   image_info['image link'].append(key['links'][0]['href'])

# print(image_info)

