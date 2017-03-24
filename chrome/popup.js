var RECOMMEND_API_URL = BASE_API + '/recommend_articles'

function main() {
	var port = chrome.extension.connect({
		name: "user_id_comm"
	});
	port.onMessage.addListener(function(msg) {
		console.log("message recieved" + msg);
		storeObjectInLocalStorage("USER_ID", msg);
	});
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
    var url = tab.url;
    callback(url);
});
}

function isURLNewsSourcePromise(url) {
	return new Promise(function(resolve, reject) {
		$.get(CONSTANTS.IS_NEWS_SOURCE_API, {'url': url}, function(response) {
			response = JSON.parse(response);
			var error = response.error;
			if (error || !response.is_news_article) reject();
			else resolve();
		});
	});
}

/**
 * @param {string} article_url = the url of the current article
 * @param {function(string,number,number)} callback - Called when dictionary has
 *   been recieved.
 * @param {function(string)} errorCallback - Called when the dictionary is not received properly.
 *   The callback gets a string that describes the failure reason.
 */
function getArticleSuggestions(article_url, callback, errorCallback) {
	isURLNewsSourcePromise(article_url).then(function () {
		$.get(RECOMMEND_API_URL, {'url': article_url}, function(data, error) {
			if (error) errorCallback('Network error');
			callback(data);
		});  
	}, function() {
		$('h2').html('Not a news site');
	});
}

function displayArticles(suggestedArticles) {
	var ul = document.getElementById('suggested_list');
  	var li_arr = ul.getElementsByTagName('li');
  	var count = 0;
	suggestedArticles.forEach(function(article){
	var li = li_arr[count];
    var _img = li.children[0];
    _img.src = getSiteFavicon(article['url']);
    _img.height = "50";
    _img.width = "50";
    var a = li.children[1];
	a.href = article['url'];
	a.addEventListener("click", getCurrentTabUrl(sendArticleWasClicked));
	a.target = "_blank";
	a.textDecoration = "none";
    a.innerHTML = article['title'];
    count++;
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
      		console.log('error: ' + errorMessage);
		});
	}
		getCurrentTabUrl(sendArticlesWereDisplayed);
}

function sendArticlesWereDisplayed(url) {
	var userID = getObjectFromLocalStorage("USER_ID");
	var API_URL = BASE_API + '/suggestions_received'
	$.post(API_URL, {'url': url, 'id': userID}, function(data, error) {
		console.log(data);
	});  
}

function sendArticleWasClicked(url) {
	console.log("article clicked");
	var userID = getObjectFromLocalStorage("USER_ID");
	var API_URL = BASE_API + '/suggestion_clicked'
	$.post(API_URL, {'url': url, 'id': userID}, function(data, error) {
		console.log(data);
	});  
}

function addChromeExtensionOpenedListener() {
	document.addEventListener('DOMContentLoaded', function() {
		getCurrentTabUrl(
			getSuggestionsAndDisplayArticles
		);
	});  
}

