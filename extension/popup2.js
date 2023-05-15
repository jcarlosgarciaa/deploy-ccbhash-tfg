const confirma = document.getElementById("confirma")
confirma.addEventListener("click", () => {
    chrome.runtime.sendMessage({selection: "1"}, function (response) {
        window.close()
    });

})

const cancela = document.getElementById("cancelar")
cancela.addEventListener("click", () => {
  chrome.runtime.sendMessage({selection: "3"}, function (response) {
    window.close()
    
});
})
window.addEventListener('load', function() {
    chrome.runtime.sendMessage({selection: "4"}, function (response) {
        const dat = response.data;
        let info = "";
    
        if (dat.exists === true){
            info = `El archivo ${dat.filename} ya existe en la base de datos y está etiquetado como ${dat.malware} malware`;
        } else {
            if (dat.malware === "si"){
                info = `El archivo ${dat.filename} con el malware que más similitud tiene es con ${dat.file} con una similitud de ${(dat.similarity * 100).toFixed(2)}%. Por tanto, puede considerarse como malware`;
            } else if (dat.malware === "sospechoso"){
                info = `El archivo ${dat.filename} con el malware que más similitud tiene es con ${dat.file} con una similitud de ${(dat.similarity * 100).toFixed(2)}%. Por tanto, puede considerarse como SOSPECHOSO de ser malware`;
            } else {
                info = `El archivo ${dat.filename} con el malware que más similitud tiene es con ${dat.file} con una similitud de ${(dat.similarity * 100).toFixed(2)}%. Por tanto, NO puede considerarse como malware`;
            }
        }
    
        if (dat.error){
            info = `ERROR: Se ha encontrado un error analizando el archivo ${dat.filename}`;
            document.getElementById("RES").style.visibility = 'hidden';
        }
    
        document.getElementById("text").innerHTML = info;
    });
});

