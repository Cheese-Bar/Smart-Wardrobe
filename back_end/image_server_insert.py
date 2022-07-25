from PIL import Image
import psycopg2 as ps
import os
from io import StringIO, BytesIO 

def insert_img():
    #insert and store image with binary format
    conn = ps.connect(host="127.0.0.1", user="postgres", password="postgres", database="asoct")#connect postgresql 
    if conn is not None:
        cur = conn.cursor()
        image_dir = '/data/fjsdata/ASOCT/Cataract/C_8bit_Crop_New' #the path of images
        for fname in sorted(os.listdir(image_dir)):
            if fname.endswith(".jpg"):
                #open the image file 
                with open(os.path.join(image_dir, fname),'rb') as reader:
                    img_buffer = reader.read()     
                command = "insert into cataract(name, content) values(%s, %s);"#create table cataract
                params = (fname, ps.Binary(img_buffer))
                cur.execute(command, params)
                conn.commit()# commit the changes
        cur.close()# close communication with the PostgreSQL database server
        conn.close()

def get_image():
    #query and show image
    conn = ps.connect(host="127.0.0.1", user="postgres", password="postgres", database="asoct")#connect postgresql 
    if conn is not None:
        cur = conn.cursor() 
        command = "select * from cataract limit 1;"
        cur.execute(command)    
        rcd = cur.fetchone()
        img_name = rcd[0]#get name
        img_data = rcd[1]#get content
        print (img_name)
        img = Image.open(BytesIO(img_data))
        #img.save(img_name)
        img.show()