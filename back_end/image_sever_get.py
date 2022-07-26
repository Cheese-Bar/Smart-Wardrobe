from io import StringIO,BytesIO 
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