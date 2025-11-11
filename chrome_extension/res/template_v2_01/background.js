
// console.log('[background.js] starting..')

chrome.tabs.create({url:chrome.extension.getURL("js/main.html")}, function(tab) {
  console.log(chrome.tabs)
});


