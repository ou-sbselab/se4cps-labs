# Modification of https://github.com/DexterInd/GoogleVisionTutorials/

# Assumes that images exist in the ./img directory

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import json
import base64
import os
import argparse

parser = argparse.ArgumentParser(description='Lab 6')
parser.add_argument('--run_type', default="logo", help="logo|label|facial")

# This function has two purposes:
# if args.run_type == logo, then classify logos in the img/logos folder
# otherwise, run a classifier on the images in img/classify folder
def main(run_type):

  # Get credentials
  credentials = GoogleCredentials.get_application_default()
  service     = discovery.build('vision', 'v1', credentials=credentials)

  # Classify logos
  if run_type == "logo":
    print "Classifying logos"
    print "------"
    for dirpath,dirs,files in os.walk('img/logos'):
      for f in files:
        if f.endswith('.jpg') or f.endswith('.png'):
          with open(os.path.join(dirpath,f),'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
              'requests': [{
                'image': {
                  'content': image_content.decode('UTF-8')
                },
                'features': [{
                  'type':'LOGO_DETECTION',
                  'maxResults': 1
                }]
              }]
            })
            response = service_request.execute()
  
            try:
              label = response['responses'][0]['logoAnnotations'][0]['description']
            except:
              label = 'No response'
  
            print "Image [%s] has label [%s]" % (f, label)

  else:

    if run_type == "facial":
      folder = "facial"
      classify_type = "FACE_DETECTION"
    else:
      folder = "classify"
      classify_type = "LABEL_DETECTION"

    print "Classifying images in folder [img/%s]" % folder
    print "------"
    for dirpath,dirs,files in os.walk('img/%s' % folder):
      for f in files:
        if f.endswith('.jpg') or f.endswith('.png'):
          with open(os.path.join(dirpath,f),'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
              'requests': [{
                'image': {
                  'content': image_content.decode('UTF-8')
                },
                'features': [{
                  'type':'%s'%classify_type,
                  'maxResults': 1
                }]
              }]
            })
            response = service_request.execute()
            print f
            print json.dumps(response, indent=4, sort_keys=True)
            print "-"


# Main function
if __name__ == "__main__":
  args = parser.parse_args()
  main(args.run_type)
