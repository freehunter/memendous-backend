from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import boto3
import base64
from boto3 import client

import os
import io

# def meme(event, context):
#     user_download_img ='meme.jpg'
#     print('user_download_img ==> ',user_download_img)

#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket(u'memendous') 
#     obj = bucket.Object(key=user_download_img)      #pass your image Name to key
    
#     response = obj.get()     #get Response
#     img = response[u'Body'].read()        # Read the respone, you can also print it.
#     print(type(img))                      # Just getting type.
#     myObj = [base64.b64encode(img)]          # Encoded the image to base64

#     print(type(myObj))            # Printing the values
#     print(myObj[0])               # get the base64 format of the image
#     print('type(myObj[0]) ================>',type(myObj[0]))

#     return_json = str(myObj[0])           # Assing to return_json variable to return.  
#     print('return_json ========================>',return_json)

#     return_json1 = return_json.replace("b'","")          # repplace this 'b'' is must to get absoulate image.
#     encoded_image = return_json1.replace("'","")   

#     s3 = boto3.resource('s3')
#     object = s3.Object('my_bucket_name', 'my/key/including/filename.txt')
#     object.put(Body=some_binary_data)





def meme(event, context):
    # bucketname = 'memendous' # replace with your bucket name
    # filename = 'background.png' # replace with your object key
    # s3 = boto3.resource('s3')
    # s3.Bucket(bucketname).download_file(filename, '/tmp/meme.png')
    
    base_path = os.environ['IMAGES_DIR']
    
    print(f'{base_path}background.png')
    
    base_img = f'{base_path}background.png'
  
    base = Image.open(base_img).convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    # fnt = ImageFont.truetype('Arial', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,10), "Hello", fill=(255,255,255,128))
    # draw text, full opacity
    d.text((10,60), "World", fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)

    out.save('/tmp/greeting_card.png')
    
    print("made the image, now to upload it")
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file('/tmp/greeting_card.png', 'memendous', 'greeting_card.png')
    except:
        print("error")
        return False
    return True
    
    # object = s3.Object('memendous', '/tmp/greeting_card.png')
    # object.put(Body=out)
    
    return out