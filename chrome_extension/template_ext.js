function chrome_tabs_create(opt) {
	return new Promise(resolve => {
		chrome.tabs.create(opt, tab => resolve(tab));
	});
  }

  function chrome_tabs_get(tabId) {
	return new Promise(resolve => {
		chrome.tabs.get(tabId, tab => resolve(tab));
	});
  }
  function chrome_tabs_getCurrent() {
	return new Promise(resolve => {
		chrome.tabs.getCurrent(tab => resolve(tab));
	});
  }
  function chrome_tabs_duplicate(tabId) {
	return new Promise(resolve => {
		chrome.tabs.duplicate(tabId, tab => resolve(tab));
	});
  }
  function chrome_tabs_getSelected(winId) {
	return new Promise(resolve => {
		chrome.tabs.getSelected(winId, tab => resolve(tab));
	});
  }
  function chrome_tabs_getAllInWindow(winId) {
	return new Promise(resolve => {
		chrome.tabs.getAllInWindow(winId, tabs => resolve(tabs));
	});
  }
  function chrome_tabs_query(queryInfo) {
	return new Promise(resolve => {
		chrome.tabs.query(queryInfo, tabs => resolve(tabs));
	});
  }
  function chrome_tabs_update(tabId, updateProperties) {
	return new Promise(resolve => {
		chrome.tabs.update(tabId, updateProperties, tab => resolve(tab));
	});
  }
  function chrome_tabs_move(tabIds, updateProperties) {
	return new Promise(resolve => {
		chrome.tabs.move(tabIds, updateProperties, tabs => resolve(tabs));
	});
  }
  function chrome_tabs_discard(tabId) {
	return new Promise(resolve => {
		chrome.tabs.discard(tabId, tab => resolve(tab));
	});
  }
  function chrome_tabs_onCreated_addListener() {
	return new Promise(resolve => {
		chrome.tabs.onCreated.addListener(tab => resolve(tab));
	});
  }



  function chrome_windows_get(windowId, getInfo) {
	return new Promise(resolve => {
		chrome.windows.get(windowId, getInfo, window => resolve(window));
	});
  }
  function chrome_windows_getCurrent(getInfo) {
	return new Promise(resolve => {
		chrome.windows.getCurrent(getInfo, window => resolve(window));
	});
  }
  function chrome_windows_getLastFocused(getInfo) {
	return new Promise(resolve => {
		chrome.windows.getLastFocused(getInfo, window => resolve(window));
	});
  }
  function chrome_windows_getAll(getInfo) {
	return new Promise(resolve => {
		chrome.windows.getAll(getInfo, window => resolve(window));
	});
  }
  function chrome_windows_create(createData) {
	return new Promise(resolve => {
		chrome.windows.create(createData, window => resolve(window));
	});
  }
  function chrome_windows_update(windowId, updateInfo) {
	return new Promise(resolve => {
		chrome.windows.update(windowId, updateInfo, window => resolve(window));
	});
  }



  function chrome_sessions_getRecentlyClosed(filter) {
	return new Promise(resolve => {
		chrome.sessions.getRecentlyClosed(filter, sessions => resolve(sessions));
	});
  }
  function chrome_sessions_getDevices(filter) {
	return new Promise(resolve => {
		chrome.sessions.getDevices(filter, devices => resolve(devices));
	});
  }
  function chrome_sessions_restore(sessionId) {
	return new Promise(resolve => {
		chrome.sessions.restore(sessionId, restoredSession => resolve(restoredSession));
	});
  }



  function chrome_management_getAll() {
	return new Promise(resolve => {
		chrome.management.getAll(result => resolve(result));
	});
  }
  function chrome_management_get(id) {
	return new Promise(resolve => {
		chrome.management.get(id, result => resolve(result));
	});
  }
  function chrome_management_getSelf() {
	return new Promise(resolve => {
		chrome.management.getSelf(result => resolve(result));
	});
  }
  function chrome_management_generateAppForLink(url, title) {
	return new Promise(resolve => {
		chrome.management.generateAppForLink(url, title, result => resolve(result));
	});
  }

  function chrome_webNavigation_getAllFrames(details) {
	return new Promise(resolve => {
		chrome.webNavigation.getAllFrames(details, result => resolve(result));
	});
  }
  function chrome_webNavigation_getFrame(details) {
	return new Promise(resolve => {
		chrome.webNavigation.getFrame(details, result => resolve(result));
	});
  }


  function chrome_processes_getProcessIdForTab(tabId) {
	return new Promise(resolve => {
		chrome.processes.getProcessIdForTab(tabId, processId => resolve(processId));
	});
  }
  function chrome_processes_getProcessInfo(processId,includeMemory) {
	return new Promise(resolve => {
		chrome.processes.getProcessInfo(processId,includeMemory, processes => resolve(processes));
	});
  }

function chrome_tabs_group(opts) {
	return new Promise(resolve => {
		chrome.tabs.group(opts, groupId => resolve(groupId));
	});
	}

async function poc(){

<extfuzzer>
	
	}
poc();
	