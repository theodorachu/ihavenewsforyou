function storeObjectInLocalStorage(key, item) {
	localStorage.setItem(key, JSON.stringify(item));
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

CONSTANTS = {
	'PREV_URL_KEY': 'prev_url'
}

// Helper method that prints the contents of local storage
function _printLocalStorage() {
	console.log("Printing Local Storage");
	for (var i = 0; i < localStorage.length; i++) {
		var key = localStorage.key(i);
		console.log(key + ": " + localStorage.getItem(key));
	}
}