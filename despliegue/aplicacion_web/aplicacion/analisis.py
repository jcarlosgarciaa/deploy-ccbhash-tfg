import os
import pymongo
import hashlib
from . import ccbhash
from bson.objectid import ObjectId

def sha512(fichero):
    fp = open(fichero, "rb")
    buffer = fp.read()
    # sha512
    hashObj = hashlib.sha512()
    hashObj.update(buffer)
    lastHash = hashObj.hexdigest().upper()
    sha512 = lastHash
    fp.close()
    return sha512

client = pymongo.MongoClient('mongodb+srv://josec:josec@cluster0.jbetzba.mongodb.net/?retryWrites=true&w=majority')

#Define Db Name
dbname = client['administracion']



#Define Collection
collection = dbname['repository']
def analyze_ccbhash(arch, filename):
    res = {}
    f_hash = sha512(arch)
    entry = collection.find_one({"file_hash": f_hash})
    
    if entry:
        
        ccbh2 = entry["ccbhash"]
        print("Existe")
        res = { 'exists' : True,
                'filename' : filename,
                'malware' : entry["malware"]
              }
        
    else:
        ccbh2 = ccbhash.calculate_ccbhash(arch)
        print('No existe')
        if ccbh2:
            res = compare_with_malware(ccbh2, filename)
            
            record={   
                    "file_hash": f_hash,
                    "ccbhash": ccbh2,
                    "name": filename,
                    "malware": res["malware"]  
                }
            collection.insert_one(record)
                    
        else:

            res = { 'filename' : filename,
                    'error': "Imposible calcular el ccbhash"}        
    
         
    
    return res, f_hash
        
def handle_uploaded_file(f):
    dir_path = './files/'
    dest =   dir_path+f.name
    with open(dest, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    return dest  

def classify(res):
    clasificacion = ""
    if res["malware"] == "no":
        clasificacion = "no"
    elif res["malware"] == "sospechoso":
        if res["similarity"] >= 0.9:
            clasificacion = "sospechoso"
        else:
            clasificacion = "no"
    else:
        if res["similarity"] >= 0.75:
            clasificacion = "si"
        elif res["similarity"] >= 0.6 and res["similarity"] < 0.75:
            clasificacion = "sospechoso"
        else:
            clasificacion = "no"

    return clasificacion

def classify_again():
    for i in collection.find({"malware": "sospechoso"}):
        ccbh = i["ccbhash"]
        filename = i["name"]
        res = compare_with_malware(ccbh, filename)
        print("Analizado ", i["name"])
        if res["malware"] == "si":
            print("Se actualiza ", res["filename"], " ")
            clave = i['_id']
            collection.update_one({'_id': ObjectId(clave)}, { '$set': {'malware': 'si'}})


def compare_with_malware(ccbh2, filename):
    max = 0
    similarity = 0
    relative_file = ""
    res = {}
    for i in collection.find({"malware": "si"}):

        ccbh = i["ccbhash"]
                    
        [scores, similar] = ccbhash.compare_files(ccbh, ccbh2)
        if similar > max:
            max = similar
            similarity = similar
            relative_file = i["name"]
                            
    #Si tiene mayor de 0.93 de coincidencia con algun malware, es malware
    if similarity >= 0.93:
        res = {     'exists' : False,
                    'filename' : filename,
                    'file' : relative_file,
                    'similarity' : similarity,
                    'malware' : "si" } 
    #Entre 0.87 y 0.93 de coincidencia con algun malware, es sospechoso
    elif similarity >= 0.87 and similarity < 0.93:
        res = {     'exists' : False,
                    'filename' : filename,
                    'file' : relative_file,
                    'similarity' : similarity,
                    'malware' : "sospechoso" }                
    #Menos de 0.6 de coincidencia con algun malware, no es malware   
    else:
                
        res = {     'exists' : False,
                    'filename' : filename,
                    'file' : relative_file,
                    'similarity' : similarity,
                    'malware' : "no" } 
    return res


def save_malware(list):
    for file in list:
        if file.endswith('.exe') or file.endswith('.ddl'):
            dir_path = './files/'
            path = dir_path + file
            print(path)
            f_hash = sha512(path)
            entry = collection.find_one({"file_hash": f_hash})
    
            if entry:
                print("Existe")
                
            else:
                print("No existe")
                print('Calculating ccbhash...')
                ccbh = ccbhash.calculate_ccbhash(path)
                if(ccbh != {}):
                    print('Analysed')
                    name = file
                    record={
                            
                        "file_hash": f_hash,
                        "ccbhash": ccbh,
                        "name": name,
                        "malware": "si"
                        
                    }
                    collection.insert_one(record)

    print(f'Save malware completed')
    