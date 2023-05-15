
let respuesta = {}
let windowCreada
let item = {}
//diccionario para drealcionar item y window 1
var dict1 = {}
//diccionario para drealcionar item y window 2
var dict2 = {}
var respuestas = {}

chrome.downloads.onDeterminingFilename.addListener(function (downloadItem) {

  //paramos descarga si es posible.
    if(downloadItem.fileSize < 20971520 && ( downloadItem.filename.endsWith('.exe') || downloadItem.filename.endsWith('.dll') )){
    chrome.downloads.pause(downloadItem.id);
    console.log(downloadItem.filename)

    console.log(downloadItem.url)

    item  = downloadItem;

    //Primer popup
    chrome.windows.create({
        focused: true,
        width: 400,
        height: 400,
        type: 'popup',
        url: 'popup1.html',
        top: 0,
        left: 0
      },
      (window) => {
        //Relacionamos item con esta ventana que creamos
        dict1[window.id] = item
      })


    }
  });


  chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    
    if (request.selection == "0"){
        //Se avisa al la ventana para que se cierre
        sendResponse({
            response: "Message received"
        });
        var url = 'https://127.0.0.1:8000/ccbhash/';
        console.log(item)
        itemEnviar = dict1[sender.tab.windowId]
        enviarUrl = itemEnviar.url
        
        
        fetch(itemEnviar.url)
        .then(response => response.blob())
        .then(blob => {
          const formData = new FormData();
          formData.append(item.filename, blob, item.filename);
          return fetch(url, {
            method: "POST",
            body: formData
          })
            .then(response => response.json())
            .then(data => {
                respuesta = data;
                console.log(data); // do something with the JSON data
                var title = "Resultados de analisis de " + data.filename;
                var message = "El archivo " + data.filename + " tiene una coincidencia de " + data.similarity + " con " + data.file + " que " + data.malware + " es malware ";

                chrome.windows.create({
                    focused: true,
                    width: 400,
                    height: 400,
                    type: 'popup',
                    url: 'popup2.html',
                    top: 0,
                    left: 0
                  },
                  (window) => {
                    //Cogemos el item relacionado con la ventana que ha mandado el mensaje
                    var did = dict1[sender.tab.windowId]
                    //El item lo relacionamos con la nueva ventana que creamos
                    dict2[window.id] = did.id
                    respuestas[window.id] = data
                    windowCreada = window
                    
                  })

                  
            })
            .catch(error => {
                
                chrome.windows.create({
                  focused: true,
                  width: 400,
                  height: 400,
                  type: 'popup',
                  url: 'popup3.html',
                  top: 0,
                  left: 0
                },
                (window) => {
                  //Cogemos el item relacionado con la ventana que ha mandado el mensaje
                  var did = dict1[sender.tab.windowId]
                  //El item lo relacionamos con la nueva ventana que creamos
                  dict2[window.id] = did.id
                  
                })
            });
        })
        .then(response => {
          console.log("File uploaded successfully");
          //Aqui llamo al segundo popup pero eso se deberia hacer cuando se reciba respuesta

        })
        .catch(error => {
          console.error("Error uploading file: ", error);
          chrome.windows.create({
            focused: true,
            width: 400,
            height: 400,
            type: 'popup',
            url: 'popup4.html',
            top: 0,
            left: 0
          },
          (window) => {
            //Cogemos el item relacionado con la ventana que ha mandado el mensaje
            var did = dict1[sender.tab.windowId]
            //El item lo relacionamos con la nueva ventana que creamos
            dict2[window.id] = did.id
            
          })

        });

        
    } else if (request.selection == "1") {
   //Se avisa a la ventana para que se cierre
        sendResponse({
            response: "Message received"
        });
        console.log("Se procede descargarlo");
        
        try {
            var itemId = dict2[sender.tab.windowId]
       chrome.downloads.search({id: itemId}, function(downloads) {
            if(downloads && downloads.length > 0) {
                console.log(downloads[0])
                if(downloads[0].canResume){
                    chrome.downloads.resume(downloads[0].id);
                }else{
                    console.log('Ya estaba descargado')
                }
                
            }
      })
        } catch (err) {
            console.log(err)
        }
        
    }else if (request.selection == "2") {
   //Opcion 2: no se quiere enviar a analizar
   //Se avisa a la ventana para que se cierre
   sendResponse({
    response: "Message received"
   });
   
   try {
    var itemId = dict1[sender.tab.windowId]
chrome.downloads.search({id: itemId.id}, function(downloads) {
    if(downloads && downloads.length > 0) {
        console.log(downloads[0])
        if(downloads[0].state == "in_progress"){
            chrome.downloads.resume(downloads[0].id);
        }
        
    }
  })
  } catch (err) {
    console.log(err)
  }


    }else if (request.selection == "3") {
  //Opcion 2: una vez tenemos los resultados, no se quiere terminar de descargar
   //Se avisa a la ventana para que se cierre
   sendResponse({
    response: "Message received"
  });
  
  try {
    var itemId = dict2[sender.tab.windowId]
    chrome.downloads.search({id: itemId}, function(downloads) {
    if(downloads && downloads.length > 0) {
        console.log(downloads[0])
        if(downloads[0].state == "in_progress"){
            console.log("El downloads es: ")
            console.log(downloads[0])
            chrome.downloads.cancel(downloads[0].id);
        }else if(downloads[0].state == "complete"){
            console.log("El downloads complete es: ")
            console.log(downloads[0])
            chrome.downloads.removeFile(downloads[0].id);
        }  
    }
  })
  } catch (err) {
    console.log(err)
  }

    }else if (request.selection == "4") {
      resp = respuestas[sender.tab.windowId]
      sendResponse({
        response: "Message received",
        data: resp
    });
    
    }
        
});


