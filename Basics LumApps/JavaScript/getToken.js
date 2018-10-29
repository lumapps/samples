//Get the token of the connected_user
//Store it in a window global variable for further use if needed
//Recommended to use fetch() instead of AJAX

function getToken()
{
    if (typeof window.auth_token == 'undefined' || typeof window.auth_token == '' || window.auth_token == '')
    {
        // Dynamic URL retrieval 
        fetch('https://' + window.location.hostname + '/service/user/token',
            {
                method: 'post',
                headers:
                {
                    "Content-Type": 'application/json;charset=UTF-8'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(function(data)
            {
                window.auth_token = data['token']
            })
            .catch(function(err)
            {
                console.log('Error ' + err)
            })
    }
};