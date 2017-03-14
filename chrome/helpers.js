function storeObjectInLocalStorage(key, item) {
	localStorage.setItem(key, JSON.stringify(item));
}

function removeObjectInLocalStorage(key){
  localStorage.removeItem(key);
}

function isKeyInLocalStorage(key) {
	return localStorage.getItem(key) !== null;
}

function getObjectFromLocalStorage(key) {
	return JSON.parse(localStorage.getItem(key));
}

function getCurrTimeAsString() {
	return new Date().toLocaleString()
}

// var _BASE_API = 'http://across-the-aisle.herokuapp.com';
var BASE_API = 'http://0.0.0.0:5000'
var CONSTANTS = {
	'ACTIVE_URLS_LS_KEY': 'active_urls',
	'TAB_URLS_LS_KEY': 'tab_urls',
	'VISITS_API': BASE_API + '/visits',
	'SUGGESTION_CLICKED_API': BASE_API + '/suggestion_clicked',
	'IS_NEWS_SOURCE_API': BASE_API + '/is_news_source'
};

var VISIT_ACTIONS = {
	SUSPEND: 'suspend',
	ACTIVATE: 'activate'
};

// Helper method that prints the contents of local storage
function _printLocalStorage() {
	console.log("Printing Local Storage");
	for (var i = 0; i < localStorage.length; i++) {
		var key = localStorage.key(i);
		console.log(key + ": " + localStorage.getItem(key));
	}
}

function getUserId(){
  return getObjectFromLocalStorage("userId");
}

function getSiteFavicon(url){
	return url.split('/')[2] + "/favicon.ico";
}