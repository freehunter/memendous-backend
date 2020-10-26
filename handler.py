# From the Lambda layer
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# AWS imports
import boto3
from boto3 import client

# Python standard library imports
import os
import io
import uuid
import base64
import json

def meme(event, context):
    
    try:
        top_text = json.dumps(event['queryStringParameters']['top']).strip('\"')
    except:
        top_text = "lol i forgot"
    try:
        bottom_text = json.dumps(event['queryStringParameters']['bottom']).strip('\"')
    except:
        bottom_text = "to add any text"
    
    #TODO
    # 1. Read images from S3
    # 2. Put text in correct place
    # 3. Center/wrap text if needed (https://www.haptik.ai/tech/putting-text-on-images-using-python-part2/)
    # 4. Make UI in JS or Vue
    # 5. Deploy UI to Amplify
    
    base_path = os.environ['IMAGES_DIR']
    
    print(f'{base_path}background.png')
    
    base_img = f'{base_path}background.png'
  
    base = Image.open(base_img).convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype(f'{base_path}font/Roboto-Bold.ttf', size=45)
    #fnt = ImageFont.truetype(f'{base_path}font/Roboto-Black.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    if top_text != "":
        d.text((10,10), top_text, font=fnt, fill=(255,255,255,128))
    else: 
        d.text((10,10), "lol i forgot", font=fnt, fill=(255,255,255,128))
    if bottom_text != "":
        # draw text, full opacity
        d.text((10,60), bottom_text, font=fnt, fill=(255,255,255,255))
    else:
        d.text((10,60), "to add text here", font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)
    
    # Generate a UUID for the name
    meme_name = uuid.uuid4()

    out.save(f'/tmp/{meme_name}.png')
    
    print("made the image, now to upload it")
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(f'/tmp/{meme_name}.png', 'memendous', f'{meme_name}.png')
    except:
        print("error")
        return False
    return {
        'statusCode': 200,
        'body': json.dumps(f'https://memendous.s3.us-east-2.amazonaws.com/{meme_name}.png')
    }
