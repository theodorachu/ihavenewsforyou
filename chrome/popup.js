// Event listener for clicks on links in a browser action popup.
// Open the link in a new tab of the current window.
function onAnchorClick(event) {
  chrome.tabs.create({ url: event.srcElement.href });
  return false;
}

//TODO: apostrophe's
function buildDummySites(){
	var dummySites = [
	{url:"http://www.nationalreview.com/article/444370/donald-trump-refugee-executive-order-no-muslim-ban-separating-fact-hysteria",
	title:"Trumps Executive Order on Refugees, Separating Fact from Hysteria"},
	{url:"https://www.wsj.com/articles/trump-blames-protesters-delta-sen-charles-schumer-for-airport-chaos-1485781646",
	title:"White House Rebuffs Criticism of Travel Ban"}
	]
	return dummySites;
}

// Given an array of URLs, build a DOM list of these URLs in the
// browser action popup.
function buildPopupDom(realSites) {
  var dummySites = buildDummySites();
  var popupDiv = document.getElementById('suggested_div');
  var ol = popupDiv.appendChild(document.createElement('ol'));

  for (var i = 0; i < dummySites.length; i++) {
    var li = ol.appendChild(document.createElement('li'));
    var a = li.appendChild(document.createElement('a'));
    a.href = dummySites[i].url;
    a.appendChild(document.createTextNode(dummySites[i].title));
    a.addEventListener('click', onAnchorClick);
  }
}

//builDummySites(buildPopUpDom);
chrome.topSites.get(buildPopupDom);
