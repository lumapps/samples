from flask import Flask, request
import urllib2

app = Flask(__name__)

@app.route('/iframe')
def iframe():
  token = request.args.get('token')
  token = token.replace(' ', '+')
  
  url = 'https://lumsites.appspot.com/_ah/api/lumsites/v1/user/get'

  req = urllib2.Request(url, headers={
    'Content-Type': 'application/json',
    'authorization': 'Bearer {}'.format(token)
  })
  
  try: 
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page
  except urllib2.HTTPError as err:
   if err.code == 401:
      return "401"