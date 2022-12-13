import psycopg2
import pandas as pd
import getpass
import random
import tensorflow as tf
import numpy as np 
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image

db_password = getpass.getpass('Enter database password: ')
dataset_size = 100
dataset = []

try:
    connection = psycopg2.connect(user="postgres",
                                  password=str(db_password),
                                  # host="str(server)",
                                  port="5432",
                                  database="nasa")
    
    if connection:
      print('\n', 'Connection established', '\n')
    
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM data;')
    id_list = cursor.fetchall()

    for i in range(0, dataset_size):
        cursor.execute('SELECT * FROM data WHERE id = %s;', id_list[random.randrange(0, len(id_list)-1)])
        dataset.append(cursor.fetchone())

    dataset_df = pd.DataFrame.from_records(dataset, columns=['image id', 'title', 'description', 'href'])

except psycopg2.Error as e_db:
    print(e_db)

finally:
    cursor.close()
    connection.close()
    print('\n', 'Connection closed', '\n')
    
url = dataset_df['href'][3]

try:
    img = Image.open(urlopen(url))
    img_array = np.array(img)
    print(img_array.shape)

except:
    print('Not able to retrieve image from URL')

plt.imshow(img_array)
plt.axis('off')
plt.show()