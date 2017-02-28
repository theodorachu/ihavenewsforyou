var ACTIVE_URLS_KEY = CONSTANTS.ACTIVE_URLS_LS_KEY;
var TAB_URLS_KEY = CONSTANTS.TAB_URLS_LS_KEY;

function main() {
	window.onbeforeunload = function(event) {
		console.log('browser closed');
		localStorage.clear();
	};

	storeObjectInLocalStorage(ACTIVE_URLS_KEY, []);
	storeObjectInLocalStorage(TAB_URLS_KEY, {});

	chrome.tabs.onActivated.addListener(onTabOpen);
	chrome.tabs.onUpdated.addListener(onURLChange);
	chrome.tabs.onRemoved.addListener(onTabClose);
}

main();

// On tab open, we send API notice that the tab has been opened
var currURL = "";
function onTabOpen(tabInfo, unimportantInfo) {
	getCurrentURLPromise().then(function(newURL) {
		isURLNewsSourcePromise(newURL).then(function() {
			if (isURLActive(newURL)) {
				console.log('url is active');
				return;
			}
			sendTimeInToServer(newURL);
			storeURLAsActive(newURL)
			storeCurrTabURL(tabInfo.tabId);
		});
	}, function(err) {});
}

/* 1) Figure out which url was closed
 * 2) Send the time of closing to the server
 * 3) Delete the tab url info for the closed tab, then store the object again in local storage
 */
function onTabClose(tabID, removeInfo) {
	var closedURL = getObjectFromLocalStorage(TAB_URLS_KEY)[tabID];
	console.log(closedURL, 'was closed');

	isURLNewsSourcePromise(closedURL).then(function() {
		sendTimeOutToServer(closedURL);
		deleteURLStorageInfo(tabID, closedURL);
	});
}

function onURLChange(tabID, changeInfo, tab) {
	console.log('url changed');

	var tabURLs = getObjectFromLocalStorage(TAB_URLS_KEY);
	var prevURL = tabURLs[tabID];
	isURLNewsSourcePromise(prevURL).then(function() {
		sendTimeInToServer(tab.url);
		sendTimeOutToServer(prevURL);
		deleteURLStorageInfo(tabID, prevURL);
		storeCurrTabURL(tabID);
	});
}

// Deletes URL and tab from local storage in two ways:
// 1) Removes url from activeURLs
// 2) Deletes the tab storage info
function deleteURLStorageInfo(tabID, url) {
	var activeURLS = getObjectFromLocalStorage(ACTIVE_URLS_KEY);
	var urlIndex = activeURLS.indexOf(url);
	if (urlIndex > -1) {
		activeURLS.splice(urlIndex, 1); 
	}
	storeObjectInLocalStorage(ACTIVE_URLS_KEY, activeURLS);

	var tabURLs = getObjectFromLocalStorage(TAB_URLS_KEY);
	delete tabURLs[tabID];
	storeObjectInLocalStorage(TAB_URLS_KEY, tabURLs);
}

function storeCurrTabURL(tabID) {
	var tabURLs = getObjectFromLocalStorage(TAB_URLS_KEY);
	getCurrentURLPromise().then(function(url) {
		tabURLs[tabID] = url;
		storeObjectInLocalStorage(TAB_URLS_KEY, tabURLs);
	});
}

function removeHashBang(url) {
	var hashBangIndex = url.indexOf('#');
	if (hashBangIndex != -1) {
		url = url.slice(0, hashBangIndex);
	}
	return url;
}

function storeURLAsActive(url) {
	url = removeHashBang(url);
	var activeURLs = getObjectFromLocalStorage(ACTIVE_URLS_KEY);
	activeURLs.push(url);
	storeObjectInLocalStorage(ACTIVE_URLS_KEY, activeURLs);
}

function isURLActive(url) {
	url = removeHashBang(url);
	var activeURLs = getObjectFromLocalStorage(ACTIVE_URLS_KEY);
	return activeURLs.includes(url);
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





