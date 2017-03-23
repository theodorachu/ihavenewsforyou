var USER_ID = "12345";
function main() {
	chrome.tabs.onActivated.addListener(onTabOpen);
	chrome.tabs.onUpdated.addListener(onURLChange);

	if (isKeyInLocalStorage("USER_ID")) {
		USER_ID = getObjectFromLocalStorage("USER_ID");
	}
	chrome.tabs.onUpdated.addListener(extractAccessToken);
	logIn();

}

main();

function sendUserIDToPopup(userID) {
	var port = chrome.extension.connect({
		name: "user_id_comm"
	});
	port.postMessage(userID);
	console.log("user id sent");
}


function extractAccessToken(tabInfo, unimportantInfo) {
	getCurrentURLPromise().then(function(url) {
		if (!url.startsWith('https://www.facebook.com/connect/')) return;
		chrome.tabs.onUpdated.removeListener(extractAccessToken);
		var accessCode = url.slice(url.indexOf('code=') + 5);
		var graphAPIURL = `${CONSTANTS.FB_GRAPH_API}?client_id=${CONSTANTS.APP_ID}&redirect_uri=${CONSTANTS.FB_REDIRECT_URI}&client_secret=${CONSTANTS.APP_SECRET}&code=${accessCode}`
   		$.get(graphAPIURL, function(response) {
   			var accessToken = response.access_token;
   			$.get("https://graph.facebook.com/me?access_token=" + accessToken, function(response) {
   				USER_ID = response.id;
   				console.log('got user id in background', USER_ID);
   				storeObjectInLocalStorage("USER_ID", USER_ID);
   				sendUserIDToPopup(USER_ID);
   			});
   		});

   		chrome.tabs.getCurrent(function(tab) {
    		chrome.tabs.remove(tabInfo, function() { });
		});
	});
}

//Get userId from storage
//If there is no Id, redirect them to the landing page
function logIn(){
  // if(USER_ID == null) {
	var newURL = 'https://www.facebook.com/v2.8/dialog/oauth?' +
		'client_id=' + CONSTANTS.APP_ID + '&redirect_uri=' + CONSTANTS.FB_REDIRECT_URI;
	chrome.tabs.create({ url: newURL });
  // }
}

// On tab open, we send API notice that the tab has been opened
var currURL = "";
function onTabOpen(tabInfo, unimportantInfo) {
	var prevURL = currURL;
	getCurrentURLPromise().then(function(newURL) {
		if (prevURL === newURL) return;
		isURLNewsSourcePromise(prevURL).then(function() {
			sendTimeToServerPromise(prevURL, VISIT_ACTIONS.SUSPEND).then();
		});

		isURLNewsSourcePromise(newURL).then(function() {
			sendTimeToServerPromise(newURL, VISIT_ACTIONS.ACTIVATE).then();
		});
		currURL = newURL;
	}, function(err) {});
}

function onURLChange(tabID, changeInfo, tab) {
	console.log('url changed');
	isURLNewsSourcePromise(tab.url).then(function() {
		// We have to chain these because the url refreshes multiple times
		sendTimeToServerPromise(currURL, VISIT_ACTIONS.SUSPEND)
			.then(sendTimeToServerPromise(tab.url, VISIT_ACTIONS.ACTIVATE));
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
			else if (!response.is_news_article) {
				chrome.browserAction.disable();
				return;
			}
			else {
				chrome.browserAction.enable();
				resolve()
			};
		})
	});
}

function sendTimeToServerPromise(url, visitUpdateType) {
	return new Promise(function(resolve, reject) {
		var params = {
		'url': url,
		'id': USER_ID,
		'time': getCurrTimeAsString(),
		'visitUpdateType': visitUpdateType
		}
		var apiURL = CONSTANTS['VISITS_API'];
		if (!params.url) return;

		constructPostPromise(apiURL, params).then(function(response) {
			console.log(params.visitUpdateType + ':', params.url, 'sent successfully with time', params.time);
			resolve();
		}, function(error) {
			console.log(params.url, 'not sent correctly:', error);
			reject(error);
		});	
	});
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


