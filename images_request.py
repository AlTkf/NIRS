import requests
import psycopg2
from random import choice
from string import digits
import getpass
import random

def request_image(image_id):
  API_Root = "https://images-api.nasa.gov/search"
  parameters = {
      'media_type' : 'image',
      'nasa_id' : image_id
  }
  response = requests.get(API_Root, params=parameters).json()
  return response

db_password = getpass.getpass('Enter database password: ')

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

try:
    connection = psycopg2.connect(user="postgres",
                                  password=str(db_password),
                                  # host="str(server)",
                                  port="5432",
                                  database="nasa")
    
    if connection:
      print('\n', 'Connection established', '\n\n\n')
    
    cursor = connection.cursor()

    count = 0
    new_data = 10
    error_limit = 2

    id_black_list = [] # list of image ids not available (request_image() fails)
                       # or already in database (cursor.execute() fails)
    
    # def black_list(image_id, id_black_list):
    #   return image_id in id_black_list

    while count < new_data:
      data_recorded = False
      count_error = 0
      while data_recorded == False and count_error < error_limit:
        # random.seed()
        try:
            # while black_list(image_id, id_black_list):
            #   random.seed()
            #   random_number = ''.join(choice(digits) for i in range(5))
            #   image_id = 'PIA'+random_number
            random.seed()
            random_number = ''.join(choice(digits) for i in range(5))
            image_id = 'PIA'+random_number
            data = request_image(image_id)
            key = data['collection']['items'][0]
            id = key['data'][0]['nasa_id']
            title = key['data'][0]['title']
            description = key['data'][0]['description']
            href = key['links'][0]['href']
            postgres_insert_query = "INSERT INTO data (id, title, description, image_link) VALUES (%s,%s,%s,%s)"
            record_to_insert = (id, title, description, href)
            cursor.execute(postgres_insert_query, record_to_insert)
            # data_recorded = True
            print(image_id, 'recorded in database')
            count = count + 1
        
        except psycopg2.Error as e_db:
          count_error = count_error + 1
          print(image_id, e_db)
          connection.commit()
          cursor.close()
          connection.close()
          print('\n','Connection closed: unsuccesseful database query')
          connection = psycopg2.connect(user="postgres",
                                  password=str(db_password),
                                  # host="str(server)",
                                  port="5432",
                                  database="nasa")
    
          if connection:
            print('\n', 'Connection reestablished', '\n')
          
          cursor = connection.cursor()
      
        except Exception as e_data:
          count_error = count_error + 1
          print(image_id, e_data)
          id_black_list.append(image_id)

except psycopg2.Error as error:
    print('\n\n\n',"Connection error:", error.pgerror)

finally:
  connection.commit()
  cursor.close()
  connection.close()
  print('\n\n\n','Connection closed. Added %d rows' %count)
