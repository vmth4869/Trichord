
// console.log('[background.js] starting..')

chrome.tabs.create({url:"js/main.html"}, function(tab) {
  console.log(chrome.tabs)
});


