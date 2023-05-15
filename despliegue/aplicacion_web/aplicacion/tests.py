from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from io import BytesIO
from unittest.mock import ANY
import zipfile
import json 

class ViewTest(TestCase):
    def test_index_view(self):
        #Se envia peticion a la vista
        response = self.client.get('/')
        #Tiene que responder OK
        self.assertEqual(response.status_code, 200)
        #Tiene que mostrar index.html
        self.assertTemplateUsed(response, 'index.html')
        
    @patch('aplicacion.views.analisis.classify_again')
    def test_classify_again_view(self, mock_classify_again):
        #Se envia peticion a la vista
        response = self.client.get(reverse('classify_again'))
        #Se mira si redirige a index
        self.assertRedirects(response, reverse('index'))
        mock_classify_again.assert_called_once()
        
    @patch('aplicacion.views.analisis.save_malware')
    def test_send_malware_correct_view(self, mock_save_malware):
        # Creamos flujo binario de datos para el zip
        zip_stream = io.BytesIO()

        # Se crea el nuevo zip
        with zipfile.ZipFile(zip_stream, 'w') as my_zip:
            # Añade el flujo de datos al fichero zip
            my_zip.writestr('test.exe', b'content')

        # Obtiene el contenido del zip
        zip_content = zip_stream.getvalue()

        # Crea un archivo para probar a subirlo
        test_file = SimpleUploadedFile('test.zip', zip_content)

        # Hace un POST a la vista con el archivo
        response = self.client.post(reverse('send_malware'), {'miArchivo': test_file})

        # Se verifica que la respuesta redirige a index
        self.assertRedirects(response, reverse('index'))

        # Se verifica que la funcion fue llamada con los argumentos que queremos
        mock_save_malware.assert_called_once_with(list=['test.exe'])
        
    @patch('aplicacion.views.analisis.analyze_ccbhash')
    @patch('aplicacion.views.analisis.handle_uploaded_file')
    def test_ccbhash_view(self, mock_handle_uploaded_file, mock_analyze_ccbhash):
        # Indica el valor devuelto por esta funcion mock
        mock_handle_uploaded_file.return_value = '/tmp/test.txt'

        # Indica el valor devuelto por esta funcion mock
        mock_analyze_ccbhash.return_value = [{'exists': True, 'malware': False}, 'test_hash']

        # Crea un archivo para testeo
        test_file_content = b'content'
        test_file = InMemoryUploadedFile(BytesIO(test_file_content), 'miArchivo', 'test.txt', 'text/plain', len(test_file_content), None)

        # Hace una peticion POST a la vista
        response = self.client.post(reverse('ccbhash'), {'miArchivo': test_file})

        # Verifica que la respuesta es la esperada
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'exists': True, 'malware': False})

        # Comprueba que se llama a la funcion con algun argumento
        mock_handle_uploaded_file.assert_called_once_with(ANY)

        # Comprueba que la funcion se llama con los argumentos esperados
        mock_analyze_ccbhash.assert_called_once_with('/tmp/test.txt', 'miArchivo')
        
    def test_send_malware_no_file_selected(self):
        # Hace una peticion POST sin enviar ningun archivo
        response = self.client.post(reverse('send_malware'))

        # Comprueba que redirige a la pagina con error
        self.assertRedirects(response, '/?error=2')

    def test_send_malware_no_zip(self):
        # Crea un archivo el cual no es un zip
        test_file = SimpleUploadedFile('test.txt', b'content')

        # Hace un peticion POST con este archivo
        response = self.client.post(reverse('send_malware'), {'miArchivo': test_file})

        # Comprueba que es el error esperado
        self.assertRedirects(response, '/?error=1')
        
    