const confirma = document.getElementById("confirma")

var url = 'http://127.0.0.1:8000/ccbhash/';
confirma.addEventListener("click", () => {  

/*  fetch(item.referrer)
    .then(response => response.blob())
    .then(blob => {
      const formData = new FormData();
      formData.append("file", blob, item.filename);
      return fetch(url, {
        method: "POST",
        body: formData
      });
    })
    .then(response => {
      console.log("File uploaded successfully");
    })
    .catch(error => {
      console.error("Error uploading file: ", error);
    });
  const json = '{"result":'+item.filename+', "count":42}';
  fetch(url, {
        method: 'POST',
        body: JSON.parse(json)
    })
  .then(response => {
    // Do something with the response
    chrome.runtime.sendMessage({selection: "0"}, function (response) {
        console.log(response);
    });*/


        // Do something with the response
        chrome.runtime.sendMessage({selection: "0"}, function (response) {
          window.close()
          
      });

  });
 


    

const cancela = document.getElementById("cancelar")
cancela.addEventListener("click", () => {
  chrome.runtime.sendMessage({selection: "2"}, function (response) {
    window.close()
    
});
})

