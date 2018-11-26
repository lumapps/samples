import httplib2
import json
from googleapiclient.discovery import build
from oauth2client.client import OAuth2Credentials
from oauth2client.service_account import ServiceAccountCredentials

#Modify these variables and point to your current credentials. 
#Script wont work unless you do so.
CLIENT_ID = ''
CLIENT_SECRET = ''
REFRESH_TOKEN = ''

#Get your ID's 
CUSTOMER_ID = ''
INSTANCE_ID = ''
COMMUNITY_ID = ''

#Authentication
credentials = OAuth2Credentials(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                refresh_token=REFRESH_TOKEN,
                                access_token=None,
                                token_expiry=None,
                                token_uri='https://accounts.google.com/o/oauth2/token',
                                user_agent=None)
                              
http = httplib2.Http()
http = credentials.authorize(http)
#accessTokenInfo = credentials.get_access_token(http)

service = build('lumsites', 'v1', http=http, discoveryServiceUrl='https://lumsites.appspot.com/_ah/api/discovery/v1/apis/lumsites/v1/rest')

#Create your post
post = {
  'authorDetails': {
    'email': 'theAuthorEmail@email.com'
  },
  'customer' : CUSTOMER_ID,
  'instance' : INSTANCE_ID,
  'externalKey': "" , #ID of the community you are publishing to
  'postType': 'DEFAULT',
  'type': 'post',
  'title': {
    'en': 'Post Title goes here'
  },
  'content': {
    'en': 'Post Description goes here'
  },
  'feedKeys': [""], #Array of feeds that are following the community (IDs)
  'parentContentDetails': {
    'uid': COMMUNITY_ID,
    'type': 'community'
  }
}


newPost = service.community().post().save(body=post).execute()

print(newPost)