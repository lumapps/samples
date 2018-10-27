
const axios = require('axios');
const oauth = require('axios-oauth-client');
const request = require('request-promise');
const security = require('./security');

// Prepare your request
// In this case, I have placed my confidential information inside an external file called "security"
const getClientCredentials = oauth.client(axios.create(), {
  url: 'https://www.googleapis.com/oauth2/v4/token',
  grant_type: 'refresh_token',
  client_id: security.CLIENT_ID,
  client_secret: security.CLIENT_SECRET,
  refresh_token: security.REFRESH_TOKEN,
  scope: 'https://www.googleapis.com/auth/userinfo.email'
});
 
//Define your async method to request your access_token
async function getToken(){
const auth = await getClientCredentials(); 
const response = await request({
  uri: 'https://lumsites.appspot.com/_ah/api/lumsites/v1/user/get',
  qs: {
    email: 'alejandro@lumapps.com'
  },
  method: 'GET',
  json: true,            
  headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.access_token}`
  }, 
});
//Print the name of the connected user
console.log(JSON.stringify(response.fullName));
};


getToken();


