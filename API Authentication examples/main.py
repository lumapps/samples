#LumApps API Strategy 1: domain-wide authentication

import pprint
import sys

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def main(argv):
  scopes = ['https://www.googleapis.com/auth/userinfo.email']
  credentials = ServiceAccountCredentials.from_json_keyfile_name('service-account.json', scopes) #Point to your file
  credentials = credentials.create_delegated(email) #Use any email in your domain (preferably yours)

  http_auth = credentials.authorize(Http())

  service = build('lumsites', 'v1', http_auth, 'https://lumsites.appspot.com/_ah/api/discovery/v1/apis/lumsites/v1/rest')

  #list = service.instance().list().execute()
  users = service.user().search(maxResults=30,
                                firstName='Thai',
                                sortOrder='registrationDate').execute()
  print users

if __name__ == '__main__':
  main(sys.argv)