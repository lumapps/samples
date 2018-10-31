import httplib2
from googleapiclient.discovery import build
from oauth2client.client import OAuth2Credentials
from security import keys 

#I store my credentials in a separate file
#Make sure to update and use yours
CLIENT_ID = keys()['CLIENT_ID']
CLIENT_SECRET = keys()['CLIENT_SECRET']
REFRESH_TOKEN = keys()['REFRESH_TOKEN']

credentials = OAuth2Credentials(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                refresh_token=REFRESH_TOKEN,
                                access_token=None,
                                token_expiry=None,
                                token_uri='https://accounts.google.com/o/oauth2/token',
                                user_agent=None)

http = httplib2.Http()
http = credentials.authorize(http)
accessTokenInfo = credentials.get_access_token(http)

service = build('lumsites', 'v1', http=http,
discoveryServiceUrl='https://lumsites.appspot.com/_ah/api/discovery/v1/apis/lumsites/v1/rest')

# Get the current user
# currentUser = service.user().get().execute()
# print ('Current user email: %s' % currentUser.get('email'))

#Step 1
#Create a bucket for your metadata
bucket_body = {
  'customer': 'your Customer_Id', #Update this with yours
  'instance': 'your Instance_Id', #Update this with yours
  'name': {
    'en': 'New bucket name here'
  }
}

bucket = service.metadata().save(body=bucket_body).execute()
familyKey = bucket['familyKey']

#Step 2
#Mass Add metadata to your bucket
#All you need to do is to add the metadata keywords into the metadataList array
metadataList = ['fill', 'this', 'array', 'with', 'all', 'the', 'metadata', 'you want to upload']

for item in metadataList:
  metadata_body = {
    'customer': 'your Customer_Id', #Update this with yours
    'instance': 'your Instance_Id', #Update this with yours
    'name': {
      'en': item
    },
    'parent': familyKey
  }
  newMetadata = service.metadata().save(body=metadata_body).execute()

print('All metadata uploaded')