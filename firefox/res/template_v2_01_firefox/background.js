
// console.log('[background.js] starting..')
dump("FUZZ_EXT_ALIVE\n");

browser.tabs.create({url:"js/main.html"}, function(tab) {
  console.log(browser.tabs)
});

browser.tabs.create({url:"js/main.html"}, function(tab) {
  console.log(browser.tabs)
});

