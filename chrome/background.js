var ACTIVE_URLS_KEY = CONSTANTS.ACTIVE_URLS_LS_KEY;
var TAB_URLS_KEY = CONSTANTS.TAB_URLS_LS_KEY;

//facebook login
var url_login_success = 'www.facebook.com/connect/login_success.html';

function main() {
	chrome.tabs.onActivated.addListener(onTabOpen);
	chrome.tabs.onUpdated.addListener(onURLChange);
}

main();

// On tab open, we send API notice that the tab has been opened
var currURL = "";
function onTabOpen(tabInfo, unimportantInfo) {
	var prevURL = currURL;
	getCurrentURLPromise().then(function(newURL) {
		if (prevURL === newURL) return;
		isURLNewsSourcePromise(prevURL).then(function() {
			sendTimeOutToServer(prevURL);
		});

		isURLNewsSourcePromise(newURL).then(function() {
			sendTimeInToServer(newURL);
		});
		currURL = newURL;
	}, function(err) {});
}

function onURLChange(tabID, changeInfo, tab) {
	console.log('url changed');
	isURLNewsSourcePromise(tab.url).then(function() {
		sendTimeInToServer(tab.url);
		sendTimeOutToServer(currURL);
		currURL = tab.url;
	});
}

function removeHashBang(url) {
	var hashBangIndex = url.indexOf('#');
	if (hashBangIndex != -1) {
		url = url.slice(0, hashBangIndex);
	}
	return url;
}

function constructPostPromise(apiURL, params) {
	return new Promise(function(resolve, reject) {
		$.post(apiURL, params, function(response) {
			response = JSON.parse(response);
			var error = response["error"];
			if (error) reject(error);
			else resolve(response);
		});
	});
}

function isURLNewsSourcePromise(url) {
	return new Promise(function(resolve, reject) {
		$.get(CONSTANTS.IS_NEWS_SOURCE_API, {'url': url}, function(response) {
			response = JSON.parse(response);
			var error = response.error;
			if (error) return;
			else if (!response.is_news_article) return;
			else resolve();
		})
	});
}

function sendTimeInfoToServer(params, apiURL) {
	if (!params.url) return;
	var sendType = params.timeOut ? "time out" : "time in";
	Promise.all([isURLNewsSourcePromise(params.url), constructPostPromise(apiURL, params)]).then(function(response) {
		console.log(sendType + ':', params.url, 'sent successfully with time', params.timeOut ? params.timeOut : params.timeIn);
	}, function(error) {
		console.log(params.url, 'not sent correctly:', error);
	});	
}

function sendTimeOutToServer(url) {
	sendTimeInfoToServer({
		'url': url,
		'id': 12345,
		'timeOut': getCurrTimeAsString()
	}, CONSTANTS['VISIT_ENDED_API']);

}

function sendTimeInToServer(url){
	sendTimeInfoToServer({
		'url': url,
		'id': 12345,
		'timeIn': getCurrTimeAsString()
	}, CONSTANTS['VISIT_BEGUN_API']);
}

function getCurrentURLPromise() {
	return new Promise(function(resolve, reject) {
		var queryInfo = {
	 		active: true,
	 		currentWindow: true
	 	};
	 	chrome.tabs.query(queryInfo, function(tabs) {
	 		var tab = tabs[0];
	 		var url = removeHashBang(tab.url);
	 		resolve(url);
	 	});
	});
}

/*
* listener for login
* TODO: security
* result.accessToken
*/
// chrome.tabs.onActivated.addListener(function(){
//   chrome.storage.sync.get('accessToken', function (result) {
//     if (result != null){
//       getCurrentTabUrl(function(url){
//         if(url.indexOf(url_login_success) != -1){
//           //slightly complicated way of getting token from url
//           var params = tabs[i].url.split('#')[1];
//           var accessToken = params.split('&')[0];
//           accessToken = accessToken.split('=')[1];
        
//           chrome.storage.sync.set({'acessToken': acessToken}, function(){
//             console.log('Account info saved');
//         });
//         }
//       });
//     } else {
//       console.log('accessToken found');
//     }
//   });

// });

