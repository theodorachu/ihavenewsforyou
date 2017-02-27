var interval = null;
var updateTime = 5000; // In milliseconds
var currentTabInfo = {};
//API routes
url_visit_begun = 'http://across-the-aisle.herokuapp.com/visit_begun';
url_visit_ended = 'http://across-the-aisle.herokuapp.com/visit_ended';
url_suggestion_clicked = 'http://across-the-aisle.herokuapp.com/suggestion_clicked';
//facebook login
var url_login_success = 'www.facebook.com/connect/login_success.html';

TIME_IN = true;
//todo
user_id = 12345;


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

function sendUrl(url, isTimeIn){
  console.log('sending url');
  postURL = ""
  params = {
      'url': url,
      'id': 12345,
    }
  if (!isTimeIn) {
    postURL = url_visit_ended
    params['timeOut'] = new Date().toLocaleString()
  } else {
    postURL = url_visit_begun
    params['timeIn'] = new Date().toLocaleString()
  }
  
  $.post(postURL, params, function(data, error) {
      console.log(data);
  });  
}

prev_url = "";
//chrome.tabs.onUpdated.addListener(getCurrentTab);
chrome.tabs.onActivated.addListener(function() {
  getCurrentTabUrl(function(url) {
    if (url != prev_url && prev_url != ""){
      // We log that the user has navigated to a new page (TIME_IN) and that they left the old (!TIME_IN)
      sendUrl(prev_url, !TIME_IN);
      sendUrl(url, TIME_IN);
    }
    else sendUrl(url, TIME_IN);
    prev_url = url;
  });
});

/*
* listener for login
* TODO: security
* result.accessToken
*/
chrome.tabs.onActivated.addListener(function(){
  chrome.storage.sync.get('accessToken', function (result) {
    if (result != null){
      getCurrentTabUrl(function(url){
        if(url.indexOf(url_login_success) != -1){
          //slightly complicated way of getting token from url
          var params = tabs[i].url.split('#')[1];
          var accessToken = params.split('&')[0];
          accessToken = accessToken.split('=')[1];
        
          chrome.storage.sync.set({'acessToken': acessToken}, function(){
            console.log('Account info saved');
        });
        }
      });
    } else {
      console.log('accessToken found');
    }
  });

});

// chrome.alarms.onAlarm.addListener(function() {
//     console.log('ALARM FIRED');
//     updateURL();
// });