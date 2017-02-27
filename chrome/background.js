var interval = null;
var updateTime = 5000; // In milliseconds
var currentTabInfo = {};
//API routes
url_visit_begun = 'http://across-the-aisle.herokuapp.com/visit_begun';
url_visit_ended = 'http://across-the-aisle.herokuapp.com/visit_ended';
url_suggestion_clicked = 'http://across-the-aisle.herokuapp.com/suggestion_clicked';

TIME_IN = true;
USER_ID = 12345;

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
 function getCurrentTabUrl(callback) {
 	var queryInfo = {
 		active: true,
 		currentWindow: true
 	};
 	chrome.tabs.query(queryInfo, function(tabs) {
 		var tab = tabs[0];
 		var url = tab.url;
 		console.assert(typeof url == 'string', 'tab.url should be a string');
 		callback(url);
 	});
 }

function sendUrl(url, isTimeIn){
	var postURL = ""
	var params = {
		'url': url,
		'id': 12345,
	}
	if (!isTimeIn) {
		postURL = url_visit_ended
		params['timeOut'] = getCurrTimeAsString();
	} else {
		postURL = url_visit_begun
		params['timeIn'] = getCurrTimeAsString();
	}

	console.log('sending url to ' + postURL);
	$.post(postURL, params, function(data, error) {
		console.log(data);
	});  
}

function getPreviousTabUrl() {
	var prevURL = ""
	if (isKeyInLocalStorage(CONSTANTS['PREV_URL_KEY'])) {
		prevURL = getObjectFromLocalStorage(CONSTANTS['PREV_URL_KEY']);
	}
	return prevURL;
}

function sendArticleReadInfo() {
	getCurrentTabUrl(function(url) {
		var prevURL = getPreviousTabUrl();
		if (prevURL !== "") sendUrl(prevURL, !TIME_IN);
		sendUrl(url, TIME_IN);
		storeObjectInLocalStorage(CONSTANTS['PREV_URL_KEY'], url);
	}); 
}

function addPageRefreshListener() {
	console.log('event added');
	window.addEventListener('hashchange', function() {
		console.log('loaded');
	});  
}

function main() {
	chrome.tabs.onActivated.addListener(function() {
		sendArticleReadInfo();
		addPageRefreshListener();
	});
}

main();



