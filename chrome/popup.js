// What license?

//API routes
var recommend_url = 'http://across-the-aisle.herokuapp.com/recommend_articles'
var LOGGER = chrome.extension.getBackgroundPage();

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
    if (localStorage.getItem(url) !== null) {
      displayArticles(JSON.parse(localStorage.getItem(url)));
      console.log('hi');
    }
    console.log('here')
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
  //TODO make more exhaustive or move to backend
  var news_sites = ["nytimes", "sfchronicle", "nationalreview", "breitbart",
                    "washingtonpost"];
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

  $.get(recommend_url, {'url': article_url}, function(data, error) {
    if (error) errorCallback('Network error');
    callback(data);
  });  

}

function displayArticles(response) {
  var popupDiv = document.getElementById('suggested_div');
  var ol = popupDiv.appendChild(document.createElement('ol'));
  response.forEach(function(article){
    var li = ol.appendChild(document.createElement('li'));
    var a = li.appendChild(document.createElement('a'));
    a.href = article['url'];
    a.appendChild(document.createTextNode(article['title']));
    // a.addEventListener('click', onAnchorClick);
  });
}

/**
 * Execution starts when a page is loaded
 * Takes url response and parses it to display the list of suggested sites
 */
document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
    getArticleSuggestions(url, function(data) {
      response = JSON.parse(data);
      localStorage.setItem(url, data);
      displayArticles(response);

    }, function(errorMessage) {
      //alert('Error: ' + errorMessage);
      //TODO: present better error message, this crashes chrome
    });
  });
});
