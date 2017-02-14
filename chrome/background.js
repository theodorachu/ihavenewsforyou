var interval = null;
var updateTime = 5000; // In milliseconds
var currentTabInfo = {};
//API routes
url_visit_begun = 'https://localhost:5000/visit_begun';
url_visit_ended = 'https://localhost:5000/visit_ended';
url_suggestion_clicked = 'https://localhost:5000/suggestion_clicked';

TIME_IN = 1;
TIME_OUT = 0;
//todo
user_id = 12345;

console.log('page loaded');


var getURL = function(url) {
    chrome.storage.sync.get('trackr', function(data) {
        var index, found;

        if ($.isEmptyObject(data)) {
            currentTabInfo.id = '_' + Math.random().toString(36).substr(2, 9);
            currentTabInfo.title = new URL(url).hostname;
            currentTabInfo.time = 0;
            var obj = {
                'trackr': [{
                    'id': currentTabInfo.id,
                    'title': currentTabInfo.title,
                    'time': currentTabInfo.time
                }]
            };
            chrome.storage.sync.set(obj);
            return;
        }

        $.each(data.trackr, function(i, v) {
            if (v.title === new URL(url).hostname) {
                index = i;
                found = true;
                return false;
            }
        });

        if (found) {
            var retrieved = data.trackr[index];
            currentTabInfo.id = retrieved.id;
            currentTabInfo.title = retrieved.title;
            currentTabInfo.time = retrieved.time;
        } else {
            currentTabInfo.id = '_' + Math.random().toString(36).substr(2, 9);
            currentTabInfo.title = new URL(url).hostname;
            currentTabInfo.time = 0;

            data.trackr.push({
                'id': currentTabInfo.id,
                'title': currentTabInfo.title,
                'time': currentTabInfo.time
            });
        }

        chrome.storage.sync.set(data);
    });
};

var updateURL = function() {
    console.log('CURRENT TAB URL: ' + currentTabInfo.title);
    chrome.storage.sync.get('trackr', function(data) {
        var index;
        $.each(data.trackr, function(i, v) {
            if (v.title === currentTabInfo.title) {
                index = i;
                return false;
            }
        });
        data.trackr[index].time = data.trackr[index].time + 1;

        chrome.storage.sync.set(data);
    });
};

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

function isNewsSource(url){
  var domain;
  if (url.indexOf("://") > -1) {
    domain = url.split('.')[1];
  }
  else {
    domain = url.split('/')[0];
  }
  //TODO make more exhaustive or move to backend
  var news_sites = ["nytimes", "sfchronicle", "nationalreview", "breitbart"];
  return news_sites.includes(domain);
}

function sendUrl(url, timein){
  console.log('send url');
  if(isNewsSource(url){
  var http = new XMLHttpRequest();
  var params = 'url='+article_url+ '&id=' + user_id;
  if(timein) params += '&timeIn=' + Date.Now();
  else params += '&timeOut=' + Date.Now();
  http.open('POST', url_visit_begun, true);
  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        //TODO something on successfull response
    }
}
  x.send(params);
  }
}
prev_url = "";
//chrome.tabs.onUpdated.addListener(getCurrentTab);
chrome.tabs.onActivated.addListener(function() {
  getCurrentTabUrl(function(url) {
    if (url != prev_url){
      sendUrl(prev_url, TIME_OUT);
      sendUrl(url, TIME_OUT);
    }
    else sendUrl(url, TIME_IN);
  });
});

// chrome.alarms.onAlarm.addListener(function() {
//     console.log('ALARM FIRED');
//     updateURL();
// });