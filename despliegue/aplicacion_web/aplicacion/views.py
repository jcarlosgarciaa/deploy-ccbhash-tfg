from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import analisis
from .forms import UploadFileForm
import pymongo
import json
import os
from . import ccbhash
import datetime
import zipfile
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

client = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.jbetzba.mongodb.net/?retryWrites=true&w=majority')

#Define Db Name
dbname = client['administracion']

#Define Collection
collection = dbname['repository']

requests = dbname['requests']



def index(request):
    
    return render(request, 'index.html')

@csrf_exempt
def ccbhash(request):
    print('Se ha recibido un archivo')
    data = {}
    if request.method=='POST':
        
        form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():    
        for filename, file in request.FILES.items():
            #name = request.FILES[filename].name
            #print("filename: " + filename)
            file = request.FILES[filename]
            destination = analisis.handle_uploaded_file(file)
            print(file)
            [data, f_hash] = analisis.analyze_ccbhash(destination, filename)
            #gestionar peticion
            # Obtener la dirección IP del cliente
            ip_address = request.META.get('REMOTE_ADDR')

            # Obtener la fecha y hora actual
            now = datetime.datetime.utcnow()
                
            is_error = 'error' in data
            # Crear un objeto JSON con los datos que deseas almacenar
            if is_error:

                peticion = {
                    'ip_address': ip_address,
                    'time':  now,
                    'filename': filename,
                    'error': is_error,
                    'file_hash':f_hash
                }
            else:
                
                peticion = {
                    'ip_address': ip_address,
                    'time':  now,
                    'filename': filename,
                    'error': is_error,
                    'exists': data["exists"],
                    'malware': data["malware"],
                    'file_hash':f_hash
                }

            requests.insert_one(peticion)
            
            
            
        print('json-data to be sent: ', data)
        return HttpResponse(json.dumps(data), content_type='application/json')
    
    
def classify_again(request):
    print("Se va a recalcular el valor de los ficheros de la base de datos...")
    analisis.classify_again()
    print("Recalculado")
    return redirect('index')

def send_malware(request):
    if request.method == 'POST':
        # Check if the uploaded file is present in the request
        if 'miArchivo' in request.FILES:
            # Get the uploaded file from the request
            uploaded_file = request.FILES['miArchivo']

            # Check if the uploaded file is a zip file
            if uploaded_file.name.endswith('.zip'):
                extracted_files = []
                with zipfile.ZipFile(uploaded_file, 'r') as my_zip:
                     # Get the path to the 'zip' directory in the parent directory of this view
                    zip_dir = os.path.join(os.path.dirname(__file__), '..', 'files')

                    # Create the 'zip' directory if it does not exist
                    os.makedirs(zip_dir, exist_ok=True)
                    for file_name in my_zip.namelist():
                        if file_name.endswith('.exe') or file_name.endsWith('.ddl'):
                            my_zip.extract(file_name, path=zip_dir)

                            extracted_files.append(file_name)
                    analisis.save_malware(list=extracted_files)
                return redirect('index')
            else:
                # Redirect to an error page if the uploaded file is not a zip file
                return redirect('/?error=1')
        else:
            # Redirect to an error page if no file was selected
            return redirect('/?error=2')
    else:
        return HttpResponse('Invalid request')