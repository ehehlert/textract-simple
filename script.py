#Detects text in a document stored in an S3 bucket. Display polygon box around text and angled text 
import boto3
import io
import json
import os
from PIL import Image, ImageDraw

def process_text_detection(s3_connection, client, bucket, document, file_extension):

    #Get the document from S3  
    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    #To process using image bytes:                      
    #image_binary = stream.getvalue()
    #response = client.detect_document_text(Document={'Bytes': image_binary})

    # Detect text in the document
    # Process using S3 object
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    # Get the text blocks
    blocks=response['Blocks']
    width, height =image.size    
    print ('Detected Document Text')
   
    # Create image showing bounding box/polygon the detected lines/text
    for block in blocks:
            # Display information about a block returned by text detection
            print('Type: ' + block['BlockType'])
            if block['BlockType'] != 'PAGE':
                print('Detected: ' + block['Text'])
                print('Confidence: ' + "{:.2f}".format(block['Confidence']) + "%")

            print('Id: {}'.format(block['Id']))
            if 'Relationships' in block:
                print('Relationships: {}'.format(block['Relationships']))
            print('Bounding Box: {}'.format(block['Geometry']['BoundingBox']))
            print('Polygon: {}'.format(block['Geometry']['Polygon']))
            print()
            draw=ImageDraw.Draw(image)
            # Draw WORD - Green -  start of word, red - end of word
            if block['BlockType'] == "WORD":
                draw.line([(width * block['Geometry']['Polygon'][0]['X'],
                height * block['Geometry']['Polygon'][0]['Y']),
                (width * block['Geometry']['Polygon'][3]['X'],
                height * block['Geometry']['Polygon'][3]['Y'])],fill='green',
                width=2)
            
                draw.line([(width * block['Geometry']['Polygon'][1]['X'],
                height * block['Geometry']['Polygon'][1]['Y']),
                (width * block['Geometry']['Polygon'][2]['X'],
                height * block['Geometry']['Polygon'][2]['Y'])],
                fill='red',
                width=2)    

                 
            # Draw box around entire LINE  
            if block['BlockType'] == "LINE":
                points=[]

                for polygon in block['Geometry']['Polygon']:
                    points.append((width * polygon['X'], height * polygon['Y']))

                draw.polygon((points), outline='black')    

    # Display the image
    image.show()

    # Save the image
    processed_image_path = f'processed-image{file_extension}'
    image.save(processed_image_path)

    # Save the JSON
    json_file_path = 'detected-text.json'
    with open(json_file_path, 'w') as outfile:
        json.dump(response, outfile, indent=4, sort_keys=True, default=str)

    return len(blocks)

def main():
    session = boto3.Session(profile_name='eric-egalvanic')
    s3_connection = session.resource('s3')
    client = session.client('textract', region_name='us-east-1')
    bucket = 'egalvanic-textract'
    document = 'image.png'
    filename, file_extension = os.path.splitext(document)
    block_count=process_text_detection(s3_connection,client,bucket,document,file_extension)
    print("Blocks detected: " + str(block_count))
    
if __name__ == "__main__":
    main()
