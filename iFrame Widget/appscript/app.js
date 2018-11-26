// Google Apps Script 
// Example displaying birthdays from a google sheet
// Enable AdminDirectory API before publishing web app (Resources > Advance Google Services)

var SHEET_BIRTHDAYS = 'Birthdays';

function doGet(e) {
  var htmlBody = '';
  var token = e.parameters['token'][0].replace(/ /g, '+');
  var result = checkConnectedUser(token);
  
  if (result.status) {
    if (e.parameters['type'] == 'birthday') {
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_BIRTHDAYS);
      
      var values = sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn()).getValues();
      
      htmlBody += '<table>';
      for (var row in values) {
        var thumbnailPhotoUrl = null;
        try {
          thumbnailPhotoUrl = AdminDirectory.Users.get(values[row][2]).thumbnailPhotoUrl;
        }
        catch (error) {}
        
        htmlBody += '<tr>';
        if (thumbnailPhotoUrl) {
          htmlBody += '<td><img src="' + thumbnailPhotoUrl + '" width="50" /></td>';
        }
        else {
          htmlBody += '<td></td>';
        }
        
        htmlBody += '<td>' + values[row][0] + ' ' + values[row][1] + '</td>';
        
        htmlBody += '<td><img src="YOUR_PATH" width="30" /></td>';
        htmlBody += '</tr>';
      }
      htmlBody += '</table>';
    }
    else {
      htmlBody += 'Unrecognize parameter';
    }
  }
  else {
    htmlBody += 'Unauthorized';
  }
  
  return HtmlService.createHtmlOutput(htmlBody).setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}


// [START Authentication using token from URL paramenters]
function checkConnectedUser(token) {
  var result = {};
  var response = null;
  
  try {
    var params = {
      "method": 'GET',
      "contentType": 'application/json;charset=UTF-8',
      "headers": {
        "Authorization": "Bearer " + token
      }
    };
    
    result['response'] = JSON.parse(UrlFetchApp.fetch('https://lumsites.appspot.com/_ah/api/lumsites/v1/user/get', params));
    
    if (result.response.email.indexOf('your.domain.com') != -1) {
      result['status'] = true;
    }
    else {
      result['status'] = false;
    }
  }
  catch (error) {
    result['status'] = false;
    result['error'] = JSON.stringify(error);
  }
   return result;
}
// [END Authentication]
