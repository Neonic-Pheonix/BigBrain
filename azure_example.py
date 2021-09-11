from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

cog_key = 'COG_KEY'
cog_endpoint = 'COG_ENDPOINT'
image_path = 'IMAGE_PATH'

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))
# Read the image fileimage_path = os.path.join('data', 'ocr', 'advert.jpg')
image_stream = open(image_path, "rb")
# Use the Computer Vision service to find text in the image
read_results = computervision_client.recognize_printed_text_in_stream(image_stream)
# Process the text line by line
for region in read_results.regions:    
    for line in region.lines:        
        # Read the words in the line of text        
        line_text = ''        
        for word in line.words:            
            line_text += word.text + ' '        
            print(line_text.rstrip())
