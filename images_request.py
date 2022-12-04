import requests
import psycopg2
import socket
from random import choice
from string import digits

def request_image(image_id):
  API_Root = "https://images-api.nasa.gov/search"
  parameters = {
      'media_type' : 'image',
      'nasa_id' : image_id
  }
  response = requests.get(API_Root, params=parameters).json()
  return response

db_password = input('Enter database password: ')


# to test what happens when the requested
# data (PIA00000) is not available: no error
# but field of info is empty

# def request_image():
#   API_Root = "https://images-api.nasa.gov/search"
#   parameters = {
#       'media_type' : 'image',
#       'nasa_id' : 'PIA00000'
#   }
#
#   response = requests.get(API_Root, params=parameters).json()
#   return response
#
# data = request_image()
# print(data)

# data = request_image('PIA00001')['collection']['items'][0]

# print(data)

try:
    connection = psycopg2.connect(user="postgres",
                                  password=str(db_password),
                                  # host="str(server)",
                                  port="5432",
                                  database="nasa")
    
    if connection:
      print('\n\n\n','Connection established')
    
    cursor = connection.cursor()

    count = 0

    while count<10:
      try:
          random_number = ''.join(choice(digits) for i in range(5))
          image_id = 'PIA'+random_number
          # image_id = 'PIA0000'+str(count)
          print(image_id)
          data = request_image(image_id)
          #key = data['collection']['items'][0]
          id = data['collection']['items'][0]['data'][0]['nasa_id']
          title = data['collection']['items'][0]['data'][0]['title']
          description = data['collection']['items'][0]['data'][0]['description']
          href = data['collection']['items'][0]['links'][0]['href']
          postgres_insert_query = "INSERT INTO data (id, title, description, image_link) VALUES (%s,%s,%s,%s)"
          record_to_insert = (id, title, description, href)
          cursor.execute(postgres_insert_query, record_to_insert)
      
      except:
        print('Data non available')

      finally:
        count = count + 1

except psycopg2.Error as error:
    print('\n\n\n',"Connection error:", error.pgerror)

finally:
  connection.commit()
  cursor.close()
  connection.close()
  print('\n\n\n','Connection closed')





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

