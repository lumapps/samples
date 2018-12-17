import httplib2
from googleapiclient.discovery import build
from oauth2client.client import OAuth2Credentials

CLIENT_ID = ''
CLIENT_SECRET = ''
REFRESH_TOKEN = ''


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
currentUser = service.user().get().execute()
print ('Current user email: %s' % currentUser.get('email'))