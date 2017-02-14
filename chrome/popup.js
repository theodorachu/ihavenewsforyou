// What license?


var BKG = chrome.extension.getBackgroundPage()
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

function isNewsSource(url){
  //extract url
  var domain;
  //find & remove protocol (http, ftp, etc.) and get domain
  if (url.indexOf("://") > -1) {
    domain = url.split('.')[1];
  }
  else {
    domain = url.split('/')[0];
  }

  var news_sites = ["nytimes", "sfchronicle", "nationalreview", "breitbart"];
  return news_sites.includes(domain);
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
  var searchUrl = 'https://across-the-aisle.herokuapp.com/' + '?url=' + article_url;
  var x = new XMLHttpRequest();
  x.open('GET', searchUrl);
  // The server responds with JSON, so let Chrome parse it.
  x.responseType = 'json'; //TODO
  //x.responseType = 'text';
  
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
    getArticleSuggestions(url, function(response) {
      var popupDiv = document.getElementById('suggested_div');
      var ol = popupDiv.appendChild(document.createElement('ol'));

      for (var i = 0; i < response.urls.length; i++) {
        var li = ol.appendChild(document.createElement('li'));
        var a = li.appendChild(document.createElement('a'));
        a.href = response.urls[i];
        a.appendChild(document.createTextNode(response.Titles[i]));
        a.addEventListener('click', onAnchorClick);
      }

    }, function(errorMessage) {
      alert('Error: ' + errorMessage);
      BKG.console.log('just log');
      console.log('please log');
      //TODO: present better error message
    });
  });
});
