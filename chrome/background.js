var userId;

function main() {
	chrome.tabs.onActivated.addListener(onTabOpen);
	chrome.tabs.onUpdated.addListener(onURLChange);
  checkIfLoggedIn();
}

main();

//Get userId from storage
//If there is no Id, redirect them to the landing page
function checkIfLoggedIn(){
  var userId = getObjectFromLocalStorage("userId");
  if(userId == null){
    var newURL = "http://127.0.0.1:5000/";
    chrome.tabs.create({ url: newURL });
  }
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
			else if (!response.is_news_article) return;
			else resolve();
		})
	});
}

function sendTimeToServerPromise(url, visitUpdateType) {
	return new Promise(function(resolve, reject) {
		var params = {
		'url': url,
		'id': userId,
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

/*
* receive message with Id from webapp
*/
chrome.runtime.onMessageExternal.addListener(
  function(message, sender, sendResponse) {
    userId = message["userId"];
    if(userId == -1){
      //user clicked logout
      removeObjectInLocalStorage("userId");
    }
    storeObjectInLocalStorage("userId", userId);
    console.log("new userId stored: ", userId); 
  });

