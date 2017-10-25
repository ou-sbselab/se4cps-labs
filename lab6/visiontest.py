import base64
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision','v1',credentials=credentials)

with open('logo/image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LOGO_DETECTION',
                    'maxResults': 1
                }]
            }]
        })
        response = service_request.execute()
        
        try:
             label = response['responses'][0]['logoAnnotations'][0]['description']
        except:
             label = "No response."
        
        print label
