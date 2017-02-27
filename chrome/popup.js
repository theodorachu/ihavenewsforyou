// CONSTNATS
//API routes
var RECOMMEND_API_URL = 'http://0.0.0.0:5000/recommend_articles'

function main() {
	addChromeExtensionOpenedListener();
}

// THIS IS THE ONLY FUNCTION WE CALL
main();



/*
Important Info: chrome.tabs.query invokes the callback with a list of tabs that match the
query. When the popup is opened, there is certainly a window and at least
one tab, so we can safely assume that |tabs| is a non-empty array.
A window can only have one active tab at a time, so the array consists of
exactly one tab.

See https://developer.chrome.com/extensions/tabs#method-query
*/
 function getCurrentTabUrl(callback) {

  var queryInfo = {
  	active: true,
  	currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url; // See https://developer.chrome.com/extensions/tabs#type-Tab for tab object documentation
    callback(url);
});
}

function isNewsSource(url){
	return true; 
}

/**
 * @param {string} article_url = the url of the current article
 * @param {function(string,number,number)} callback - Called when dictionary has
 *   been recieved.
 * @param {function(string)} errorCallback - Called when the dictionary is not received properly.
 *   The callback gets a string that describes the failure reason.
 */
function getArticleSuggestions(article_url, callback, errorCallback) {
	if (!isNewsSource(article_url)) errorCallback('Not an indexed news site');
	$.get(RECOMMEND_API_URL, {'url': article_url}, function(data, error) {
		if (error) errorCallback('Network error');
		callback(data);
	});  
}

// Helper method that prints the contents of local storage
function _printLocalStorage() {
	console.log("Printing Local Storage");
	for (var i = 0; i < localStorage.length; i++) {
		var key = localStorage.key(i);
		console.log(key + ": " + localStorage.getItem(key));
	}
}

function displayArticles(suggestedArticles) {
	var popupDiv = document.getElementById('suggested_div');
	var ol = popupDiv.appendChild(document.createElement('ol'));
	suggestedArticles.forEach(function(article){
		var li = ol.appendChild(document.createElement('li'));
		var a = li.appendChild(document.createElement('a'));
		a.href = article['url'];
		a.target = "_blank";
		a.appendChild(document.createTextNode(article['title']));
	});
}



function getSuggestionsAndDisplayArticles(url) {
	if (isKeyInLocalStorage(url)) {
		console.log('got from local storage cache');
		displayArticles(getObjectFromLocalStorage(url));
	} else {
		getArticleSuggestions(url, function(data) {
			suggestedArticles = JSON.parse(data);
			storeObjectInLocalStorage(url, suggestedArticles);
			displayArticles(suggestedArticles);
		}, function(errorMessage) {
			// TODO: Brandon - Create a better error message
			//alert('Error: ' + errorMessage);
		});
	}
}

function notifyAPIChromeExtensionOpened(url) {
	
}

function addChromeExtensionOpenedListener() {
	document.addEventListener('DOMContentLoaded', function() {

		getCurrentTabUrl(
			getSuggestionsAndDisplayArticles
		);
	});  
}



