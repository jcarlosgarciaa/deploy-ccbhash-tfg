
 
 
 
 
 
 
 
 
 
 /*chrome.runtime.onMessage.addListener((obj, sender, response) => {
   

    if (type === "NEW") {
        console.log( `Download from ${downloadItem.url} +''
    +at starttime ${downloadItem.startTime}`)
    
    chrome.downloads.pause(downloadItem.id);
    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
    }
    alert("gola");
    var c = window.confirm('¿Vale?');
    if(c) {
        console.log('okey');
    }
    sleep(5000);
    resume(downloadItem);
    /*chrome.windows.create({
        focused: true,
        width: 400,
        height: 600,
        type: 'popup',
        url: 'popup.html',
        top: 0,
        left: 0
      },
      () => {})*/




/*function handleCreated(downloadItem) {
    console.log( `Download from ${downloadItem.url} +''
    +at starttime ${downloadItem.startTime}`)
    
    chrome.downloads.pause(downloadItem.id);
    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
    }
    alert("gola");
    var c = window.confirm('¿Vale?');
    if(c) {
        console.log('okey');
    }
    sleep(5000);
    resume(downloadItem);
    /*chrome.windows.create({
        focused: true,
        width: 400,
        height: 600,
        type: 'popup',
        url: 'popup.html',
        top: 0,
        left: 0
      },
      () => {})*
    
}*/
/*
function resume(downloadItem) {
    chrome.downloads.resume(downloadItem.id);
}*/
