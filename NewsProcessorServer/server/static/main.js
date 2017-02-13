console.log('is this working?');

FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
});


/*  
Response is 
{
    status: 'connected',
    authResponse: {
        accessToken: '...',
        expiresIn:'...',
        signedRequest:'...',
        userID:'...'
    }
}
*/

function statusChangeCallBack(response) {
	console.log("Response", response.form);
}