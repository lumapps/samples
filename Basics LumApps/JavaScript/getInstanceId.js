// Before you make this call, make sure to have a user token previously defined
// Let's get your instanceId and store it in a window variable

if (typeof window.instanceUID == 'undefined')
	{
        //Dynamic URL retrieval
		fetch('https://' + window.location.hostname + '/_ah/api/lumsites/v1/instance/get?slug=' + window.instanceSlug,
			{
				method: "GET",
				credentials: "same-origin",
				headers:
				{
                    //Make sure to have your token stored
					"Authorization": "Bearer " + window.auth_token
				}
			}).then(response => response.json())
			.then(data =>
			{
				window.instanceUID = data.uid
			})
	}