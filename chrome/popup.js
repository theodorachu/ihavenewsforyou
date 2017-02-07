// What license?

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });
}

/**
 * @param {string} searchTerm - the url of the current article
 * @param {function(string,number,number)} callback - Called when dictionary has
 *   been recieved.
 * @param {function(string)} errorCallback - Called when the dictionary is not received properly.
 *   The callback gets a string that describes the failure reason.
 */
function getImageUrl(searchTerm, callback, errorCallback) {
  var searchUrl = 'https://across-the-aisle.herokuapp.com/';
  //TODO include get with comonents
  //  + '?v=1.0&q=' + encodeURIComponent(searchTerm);
  var x = new XMLHttpRequest();
  x.open('GET', searchUrl);
  // The server responds with JSON, so let Chrome parse it.
  //x.responseType = 'json'; //TODO
  x.responseType = 'text';
  
  x.onload = function() {
    var response = x.response;
    /*
    if (!response || !response.responseData || !response.responseData.results ||
        response.responseData.results.length === 0) {
      errorCallback('No response from Google Image search!');
      return;
    }
    */
    callback(response);
  };
  x.onerror = function() {
    errorCallback('Network error');
  };
  x.send();
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
    getImageUrl(url, function(response) {
      var dummySites = [
      {url:"http://www.nationalreview.com/article/444370/donald-trump-refugee-executive-order-no-muslim-ban-separating-fact-hysteria",
      title:response}
      ]
      var popupDiv = document.getElementById('suggested_div');
      var ol = popupDiv.appendChild(document.createElement('ol'));

      for (var i = 0; i < dummySites.length; i++) {
        var li = ol.appendChild(document.createElement('li'));
        var a = li.appendChild(document.createElement('a'));
        a.href = dummySites[i].url;
        a.appendChild(document.createTextNode(dummySites[i].title));
        a.addEventListener('click', onAnchorClick);
      }

    }, function(errorMessage) {
      alert('Error' + errorMessage);
      //TODO: present better error message
    });
  });
});
